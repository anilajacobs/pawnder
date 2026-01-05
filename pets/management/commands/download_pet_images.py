from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from pets.models import Pet
import requests
import time


class Command(BaseCommand):
    help = 'Downloads sample photos for all pets from free APIs'

    def handle(self, *args, **kwargs):
        self.stdout.write('Downloading pet photos...\n')

        pets = Pet.objects.all()

        for pet in pets:
            self.stdout.write(f'\nProcessing {pet.name} ({pet.breed})...')

            try:
                if pet.species == 'DOG':
                    # Use Dog CEO API for dog photos
                    breed_name = pet.breed.lower().replace(' ', '-')

                    # Try to get breed-specific images
                    urls_to_try = []

                    if 'shih' in breed_name or 'shihtzu' in breed_name:
                        # Get Shih Tzu images
                        response = requests.get('https://dog.ceo/api/breed/shihtzu/images/random/3', timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            if data['status'] == 'success':
                                urls_to_try = data['message']

                    elif 'golden' in breed_name or 'retriever' in breed_name:
                        # Get Golden Retriever images
                        response = requests.get('https://dog.ceo/api/breed/retriever-golden/images/random/3', timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            if data['status'] == 'success':
                                urls_to_try = data['message']

                    else:
                        # Get random dog images
                        response = requests.get('https://dog.ceo/api/breeds/image/random/3', timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            if data['status'] == 'success':
                                urls_to_try = data['message']

                elif pet.species == 'CAT':
                    # Use placeholder cat images
                    urls_to_try = [
                        f'https://placekitten.com/600/{400 + i * 50}' for i in range(3)
                    ]

                else:
                    self.stdout.write(self.style.WARNING(f'  Skipping {pet.species}'))
                    continue

                # Download and save photos
                for idx, url in enumerate(urls_to_try[:3]):
                    photo_field = f'photo{idx + 1}'

                    try:
                        self.stdout.write(f'  Downloading photo {idx + 1}...')
                        response = requests.get(url, timeout=15)

                        if response.status_code == 200:
                            filename = f'{pet.name.lower().replace(" ", "_")}_{idx + 1}.jpg'
                            field = getattr(pet, photo_field)

                            # Delete old photo if exists
                            if field:
                                field.delete(save=False)

                            # Save new photo
                            field.save(filename, ContentFile(response.content), save=False)
                            self.stdout.write(self.style.SUCCESS(f'    ✓ Photo {idx + 1} saved'))
                            time.sleep(0.5)  # Small delay to be nice to APIs

                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'    Failed to download photo {idx + 1}: {e}'))

                pet.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Completed {pet.name}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {pet.name}: {e}'))

        self.stdout.write(self.style.SUCCESS('\n\n✅ All pet photos have been downloaded!'))
        self.stdout.write('\nYou can now see beautiful pet photos on your site!')
