from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pet, Vaccination, Match, OwnerProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = OwnerProfile
        fields = ('phone', 'address', 'city', 'state', 'zipcode', 'profile_picture')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class PetRegistrationForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = (
            'name', 'species', 'breed', 'gender', 'date_of_birth',
            'weight', 'height', 'color', 'description',
            'is_vaccinated', 'last_vaccination_date', 'health_issues', 'is_neutered',
            'is_available_for_mating', 'preferred_breed',
            'photo1', 'photo2', 'photo3', 'location'
        )
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'last_vaccination_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'health_issues': forms.Textarea(attrs={'rows': 3}),
        }


class VaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = (
            'vaccine_type', 'vaccine_name', 'date_administered',
            'next_due_date', 'veterinarian_name', 'clinic_name',
            'certificate', 'notes'
        )
        widgets = {
            'date_administered': forms.DateInput(attrs={'type': 'date'}),
            'next_due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class PetSearchForm(forms.Form):
    GENDER_CHOICES = [('', 'Any')] + Pet.GENDER_CHOICES
    SPECIES_CHOICES = [('', 'Any')] + Pet.SPECIES_CHOICES

    species = forms.ChoiceField(choices=SPECIES_CHOICES, required=False)
    breed = forms.CharField(max_length=100, required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)
    min_age = forms.IntegerField(min_value=0, required=False, label='Min Age (years)')
    max_age = forms.IntegerField(min_value=0, required=False, label='Max Age (years)')
    is_vaccinated = forms.BooleanField(required=False, label='Vaccinated Only')
    location = forms.CharField(max_length=200, required=False)
    is_available_for_mating = forms.BooleanField(required=False, initial=True, label='Available for Mating')


class MatchRequestForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Introduce your pet and why you think they would be a good match...'}),
        }
