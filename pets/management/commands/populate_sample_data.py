from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pets.models import Pet, OwnerProfile, Vaccination
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populates the database with sample pet data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...\n')

        # Create sample users
        users_data = [
            {'username': 'bella_owner', 'email': 'bella@example.com', 'first_name': 'Sarah', 'last_name': 'Johnson'},
            {'username': 'max_owner', 'email': 'max@example.com', 'first_name': 'John', 'last_name': 'Smith'},
            {'username': 'luna_owner', 'email': 'luna@example.com', 'first_name': 'Emily', 'last_name': 'Davis'},
            {'username': 'charlie_owner', 'email': 'charlie@example.com', 'first_name': 'Michael', 'last_name': 'Brown'},
        ]

        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')

                # Create owner profile
                OwnerProfile.objects.create(
                    user=user,
                    phone=f'+1-555-{random.randint(1000, 9999)}',
                    city='San Francisco' if random.random() > 0.5 else 'Los Angeles',
                    state='California',
                    zipcode=f'{random.randint(90000, 95000)}'
                )
            users.append(user)

        # Sample pet data
        pets_data = [
            {
                'owner': users[0],
                'name': 'Bella',
                'species': 'DOG',
                'breed': 'Shih Tzu',
                'gender': 'F',
                'age_years': 2,
                'weight': 5.5,
                'height': 25.0,
                'color': 'Brown and White',
                'description': 'Bella is a sweet and gentle Shih Tzu with a lovely temperament. She loves children and gets along well with other dogs. Very healthy and active!',
                'location': 'San Francisco, CA'
            },
            {
                'owner': users[1],
                'name': 'Max',
                'species': 'DOG',
                'breed': 'Shih Tzu',
                'gender': 'M',
                'age_years': 3,
                'weight': 6.0,
                'height': 26.5,
                'color': 'Black and White',
                'description': 'Max is a healthy and playful male Shih Tzu. Great pedigree, excellent temperament. Perfect for breeding with a quality female.',
                'location': 'San Francisco, CA'
            },
            {
                'owner': users[2],
                'name': 'Luna',
                'species': 'DOG',
                'breed': 'Golden Retriever',
                'gender': 'F',
                'age_years': 4,
                'weight': 28.0,
                'height': 55.0,
                'color': 'Golden',
                'description': 'Luna is a beautiful Golden Retriever with champion bloodlines. Very friendly and intelligent. Looking for a quality male for breeding.',
                'location': 'Los Angeles, CA'
            },
            {
                'owner': users[3],
                'name': 'Charlie',
                'species': 'DOG',
                'breed': 'Golden Retriever',
                'gender': 'M',
                'age_years': 5,
                'weight': 32.0,
                'height': 58.0,
                'color': 'Golden',
                'description': 'Charlie is an AKC registered Golden Retriever with excellent health records. Gentle giant, great with kids and other pets.',
                'location': 'Los Angeles, CA'
            },
            {
                'owner': users[0],
                'name': 'Mittens',
                'species': 'CAT',
                'breed': 'Persian',
                'gender': 'F',
                'age_years': 2,
                'weight': 4.0,
                'height': 25.0,
                'color': 'White',
                'description': 'Mittens is a purebred Persian cat with stunning blue eyes. Very calm and affectionate. Looking for a quality Persian male.',
                'location': 'San Francisco, CA'
            },
        ]

        for pet_data in pets_data:
            # Calculate date of birth from age
            age_years = pet_data.pop('age_years')
            date_of_birth = date.today() - timedelta(days=age_years * 365)

            pet, created = Pet.objects.get_or_create(
                owner=pet_data['owner'],
                name=pet_data['name'],
                defaults={
                    **pet_data,
                    'date_of_birth': date_of_birth,
                    'is_vaccinated': True,
                    'last_vaccination_date': date.today() - timedelta(days=random.randint(30, 180)),
                    'is_available_for_mating': True,
                }
            )

            if created:
                self.stdout.write(f'Created pet: {pet.name} ({pet.breed})')

                # Add vaccination records
                vaccine_types = ['RABIES', 'DHPP', 'BORDETELLA'] if pet.species == 'DOG' else ['RABIES', 'FVRCP', 'FELV']

                for vaccine_type in vaccine_types:
                    vacc_date = date.today() - timedelta(days=random.randint(60, 300))
                    Vaccination.objects.create(
                        pet=pet,
                        vaccine_type=vaccine_type,
                        date_administered=vacc_date,
                        next_due_date=vacc_date + timedelta(days=365),
                        veterinarian_name='Dr. Smith',
                        clinic_name='Happy Paws Veterinary Clinic'
                    )

        self.stdout.write(self.style.SUCCESS('\n✅ Sample data created successfully!'))
        self.stdout.write('\nYou can now login with any of these accounts:')
        self.stdout.write('  Username: bella_owner, max_owner, luna_owner, or charlie_owner')
        self.stdout.write('  Password: password123')
        self.stdout.write('\nOr create your own account at http://127.0.0.1:8000/register/\n')
