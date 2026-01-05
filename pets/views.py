from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Pet, Vaccination, Match, Favorite, OwnerProfile
from .forms import (
    UserRegistrationForm, OwnerProfileForm, PetRegistrationForm,
    VaccinationForm, PetSearchForm, MatchRequestForm
)


def home(request):
    """Homepage showing featured pets"""
    recent_pets = Pet.objects.filter(is_active=True, is_available_for_mating=True)[:8]
    context = {
        'recent_pets': recent_pets,
    }
    return render(request, 'pets/home.html', context)


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create owner profile
            OwnerProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Pawnder!')
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'pets/register.html', {'form': form})


@login_required
def profile(request):
    """User profile view"""
    owner_profile, created = OwnerProfile.objects.get_or_create(user=request.user)
    my_pets = Pet.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = OwnerProfileForm(request.POST, request.FILES, instance=owner_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = OwnerProfileForm(instance=owner_profile)

    context = {
        'form': form,
        'my_pets': my_pets,
        'owner_profile': owner_profile,
    }
    return render(request, 'pets/profile.html', context)


@login_required
def add_pet(request):
    """Add a new pet"""
    if request.method == 'POST':
        form = PetRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, f'{pet.name} has been added successfully!')
            return redirect('pet_detail', pk=pet.pk)
    else:
        form = PetRegistrationForm()
    return render(request, 'pets/add_pet.html', {'form': form})


@login_required
def edit_pet(request, pk):
    """Edit pet details"""
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = PetRegistrationForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, f'{pet.name}\'s profile updated successfully!')
            return redirect('pet_detail', pk=pet.pk)
    else:
        form = PetRegistrationForm(instance=pet)

    return render(request, 'pets/edit_pet.html', {'form': form, 'pet': pet})


def pet_detail(request, pk):
    """Pet detail view"""
    pet = get_object_or_404(Pet, pk=pk)
    vaccinations = pet.vaccinations.all()
    is_owner = request.user.is_authenticated and pet.owner == request.user
    is_favorited = False
    has_pending_match = False

    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, pet=pet).exists()
        if not is_owner and request.user.pets.exists():
            # Check if user has already sent a match request
            has_pending_match = Match.objects.filter(
                from_pet__owner=request.user,
                to_pet=pet
            ).exists()

    context = {
        'pet': pet,
        'vaccinations': vaccinations,
        'is_owner': is_owner,
        'is_favorited': is_favorited,
        'has_pending_match': has_pending_match,
    }
    return render(request, 'pets/pet_detail.html', context)


def search_pets(request):
    """Search pets with filters"""
    form = PetSearchForm(request.GET or None)
    pets = Pet.objects.filter(is_active=True, is_available_for_mating=True)

    if form.is_valid():
        if form.cleaned_data.get('species'):
            pets = pets.filter(species=form.cleaned_data['species'])

        if form.cleaned_data.get('breed'):
            pets = pets.filter(breed__icontains=form.cleaned_data['breed'])

        if form.cleaned_data.get('gender'):
            pets = pets.filter(gender=form.cleaned_data['gender'])

        if form.cleaned_data.get('location'):
            pets = pets.filter(location__icontains=form.cleaned_data['location'])

        if form.cleaned_data.get('is_vaccinated'):
            pets = pets.filter(is_vaccinated=True)

        # Age filtering
        if form.cleaned_data.get('min_age') is not None or form.cleaned_data.get('max_age') is not None:
            today = timezone.now().date()
            if form.cleaned_data.get('min_age') is not None:
                min_date = today - timedelta(days=form.cleaned_data['min_age'] * 365)
                pets = pets.filter(date_of_birth__lte=min_date)

            if form.cleaned_data.get('max_age') is not None:
                max_date = today - timedelta(days=form.cleaned_data['max_age'] * 365)
                pets = pets.filter(date_of_birth__gte=max_date)

    context = {
        'form': form,
        'pets': pets,
    }
    return render(request, 'pets/search.html', context)


@login_required
def add_vaccination(request, pet_pk):
    """Add vaccination record for a pet"""
    pet = get_object_or_404(Pet, pk=pet_pk, owner=request.user)

    if request.method == 'POST':
        form = VaccinationForm(request.POST, request.FILES)
        if form.is_valid():
            vaccination = form.save(commit=False)
            vaccination.pet = pet
            vaccination.save()

            # Update pet vaccination status
            pet.is_vaccinated = True
            pet.last_vaccination_date = vaccination.date_administered
            pet.save()

            messages.success(request, 'Vaccination record added successfully!')
            return redirect('pet_detail', pk=pet.pk)
    else:
        form = VaccinationForm()

    return render(request, 'pets/add_vaccination.html', {'form': form, 'pet': pet})


@login_required
def send_match_request(request, pet_pk):
    """Send a match request to another pet"""
    to_pet = get_object_or_404(Pet, pk=pet_pk)

    # User must have at least one pet
    user_pets = request.user.pets.filter(is_active=True, is_available_for_mating=True)

    if not user_pets.exists():
        messages.error(request, 'You need to add a pet before sending match requests.')
        return redirect('add_pet')

    if request.method == 'POST':
        from_pet_id = request.POST.get('from_pet')
        from_pet = get_object_or_404(Pet, pk=from_pet_id, owner=request.user)

        form = MatchRequestForm(request.POST)
        if form.is_valid():
            # Check if match already exists
            if Match.objects.filter(from_pet=from_pet, to_pet=to_pet).exists():
                messages.warning(request, 'You have already sent a match request for these pets.')
                return redirect('pet_detail', pk=to_pet.pk)

            match = form.save(commit=False)
            match.from_pet = from_pet
            match.to_pet = to_pet
            match.save()

            messages.success(request, f'Match request sent from {from_pet.name} to {to_pet.name}!')
            return redirect('pet_detail', pk=to_pet.pk)
    else:
        form = MatchRequestForm()

    context = {
        'form': form,
        'to_pet': to_pet,
        'user_pets': user_pets,
    }
    return render(request, 'pets/send_match_request.html', context)


@login_required
def my_matches(request):
    """View all match requests sent and received"""
    # Matches received by user's pets
    received_matches = Match.objects.filter(to_pet__owner=request.user).select_related('from_pet', 'to_pet')

    # Matches sent by user's pets
    sent_matches = Match.objects.filter(from_pet__owner=request.user).select_related('from_pet', 'to_pet')

    context = {
        'received_matches': received_matches,
        'sent_matches': sent_matches,
    }
    return render(request, 'pets/my_matches.html', context)


@login_required
def respond_to_match(request, match_pk, action):
    """Accept or reject a match request"""
    match = get_object_or_404(Match, pk=match_pk, to_pet__owner=request.user)

    if action == 'accept':
        match.status = 'ACCEPTED'
        match.save()
        messages.success(request, f'Match request accepted! You can now contact {match.from_pet.owner.get_full_name() or match.from_pet.owner.username}')
    elif action == 'reject':
        match.status = 'REJECTED'
        match.save()
        messages.info(request, 'Match request rejected.')

    return redirect('my_matches')


@login_required
def toggle_favorite(request, pet_pk):
    """Add or remove pet from favorites"""
    pet = get_object_or_404(Pet, pk=pet_pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, pet=pet)

    if not created:
        favorite.delete()
        messages.info(request, f'{pet.name} removed from favorites.')
    else:
        messages.success(request, f'{pet.name} added to favorites!')

    return redirect('pet_detail', pk=pet_pk)


@login_required
def favorites(request):
    """View all favorite pets"""
    favorite_pets = Favorite.objects.filter(user=request.user).select_related('pet')

    context = {
        'favorites': favorite_pets,
    }
    return render(request, 'pets/favorites.html', context)
