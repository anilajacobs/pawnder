from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from pets.models import Pet
import requests
import time


class Command(BaseCommand):
    help = 'Ensures all pets have 3 photos'

    def handle(self, *args, **kwargs):
        self.stdout.write('Checking and adding missing photos...\n')

        pets = Pet.objects.all()

        for pet in pets:
            # Check which photos are missing
            missing_photos = []
            if not pet.photo1:
                missing_photos.append(1)
            if not pet.photo2:
                missing_photos.append(2)
            if not pet.photo3:
                missing_photos.append(3)

            if not missing_photos:
                self.stdout.write(self.style.SUCCESS(f'✓ {pet.name} has all photos'))
                continue

            self.stdout.write(f'\n{pet.name} is missing photos: {missing_photos}')

            try:
                urls = []

                if pet.species == 'DOG':
                    if 'shih' in pet.breed.lower() or 'shihtzu' in pet.breed.lower():
                        response = requests.get('https://dog.ceo/api/breed/shihtzu/images/random/3', timeout=10)
                    elif 'golden' in pet.breed.lower() or 'retriever' in pet.breed.lower():
                        response = requests.get('https://dog.ceo/api/breed/retriever-golden/images/random/3', timeout=10)
                    else:
                        response = requests.get('https://dog.ceo/api/breeds/image/random/3', timeout=10)

                    if response.status_code == 200:
                        data = response.json()
                        if data['status'] == 'success':
                            urls = data['message']

                elif pet.species == 'CAT':
                    # Use Cat API
                    for i in range(3):
                        response = requests.get('https://api.thecatapi.com/v1/images/search', timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            if data and len(data) > 0:
                                urls.append(data[0]['url'])
                        time.sleep(0.3)

                # Download missing photos
                for i, photo_num in enumerate(missing_photos):
                    if i < len(urls):
                        url = urls[i]
                        photo_field = f'photo{photo_num}'

                        try:
                            self.stdout.write(f'  Downloading photo {photo_num}...')
                            response = requests.get(url, timeout=15)

                            if response.status_code == 200:
                                filename = f'{pet.name.lower().replace(" ", "_")}_{photo_num}.jpg'
                                field = getattr(pet, photo_field)
                                field.save(filename, ContentFile(response.content), save=False)
                                self.stdout.write(self.style.SUCCESS(f'    ✓ Photo {photo_num} saved'))
                                time.sleep(0.5)

                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f'    Failed: {e}'))

                pet.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Completed {pet.name}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {e}'))

        self.stdout.write(self.style.SUCCESS('\n\n✅ All pets now have photos!'))
