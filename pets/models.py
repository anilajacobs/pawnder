from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class OwnerProfile(models.Model):
    """Extended profile for pet owners"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='owner_profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"


class Pet(models.Model):
    """Model for pet profiles"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    SPECIES_CHOICES = [
        ('DOG', 'Dog'),
        ('CAT', 'Cat'),
        ('BIRD', 'Bird'),
        ('RABBIT', 'Rabbit'),
        ('OTHER', 'Other'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES, default='DOG')
    breed = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm", blank=True, null=True)
    color = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True, help_text="Tell us about your pet's personality")

    # Health and vaccination
    is_vaccinated = models.BooleanField(default=False)
    last_vaccination_date = models.DateField(blank=True, null=True)
    health_issues = models.TextField(blank=True, help_text="Any health concerns or special needs")
    is_neutered = models.BooleanField(default=False)

    # Breeding preferences
    is_available_for_mating = models.BooleanField(default=True)
    preferred_breed = models.CharField(max_length=100, blank=True, help_text="Preferred breed for mating")

    # Media
    photo1 = models.ImageField(upload_to='pet_photos/', blank=True, null=True)
    photo2 = models.ImageField(upload_to='pet_photos/', blank=True, null=True)
    photo3 = models.ImageField(upload_to='pet_photos/', blank=True, null=True)

    # Location
    location = models.CharField(max_length=200, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.breed})"

    @property
    def age_in_years(self):
        """Calculate pet's age in years"""
        today = timezone.now().date()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1
        return age

    @property
    def age_in_months(self):
        """Calculate pet's age in months"""
        today = timezone.now().date()
        months = (today.year - self.date_of_birth.year) * 12 + today.month - self.date_of_birth.month
        if today.day < self.date_of_birth.day:
            months -= 1
        return months


class Vaccination(models.Model):
    """Model for vaccination records"""
    VACCINE_TYPES = [
        ('RABIES', 'Rabies'),
        ('DHPP', 'DHPP (Distemper, Hepatitis, Parainfluenza, Parvovirus)'),
        ('BORDETELLA', 'Bordetella (Kennel Cough)'),
        ('LYME', 'Lyme Disease'),
        ('FVRCP', 'FVRCP (Feline Viral Rhinotracheitis, Calicivirus, Panleukopenia)'),
        ('FELV', 'FeLV (Feline Leukemia)'),
        ('OTHER', 'Other'),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='vaccinations')
    vaccine_type = models.CharField(max_length=20, choices=VACCINE_TYPES)
    vaccine_name = models.CharField(max_length=100, blank=True)
    date_administered = models.DateField()
    next_due_date = models.DateField(blank=True, null=True)
    veterinarian_name = models.CharField(max_length=100, blank=True)
    clinic_name = models.CharField(max_length=200, blank=True)
    certificate = models.FileField(upload_to='vaccination_certificates/', blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_administered']

    def __str__(self):
        return f"{self.pet.name} - {self.get_vaccine_type_display()} ({self.date_administered})"


class Match(models.Model):
    """Model for matching/interest between pets"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]

    from_pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='sent_matches')
    to_pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='received_matches')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    message = models.TextField(blank=True, help_text="Message from requester")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['from_pet', 'to_pet']

    def __str__(self):
        return f"{self.from_pet.name} → {self.to_pet.name} ({self.status})"


class Favorite(models.Model):
    """Model for favoriting pets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'pet']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} ♥ {self.pet.name}"
