from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from pets.models import Pet
import requests
import time


class Command(BaseCommand):
    help = 'Add photos specifically for Golden Retrievers'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding Golden Retriever photos...\n')

        # Specific Golden Retriever image URLs
        golden_urls = [
            'https://images.dog.ceo/breeds/retriever-golden/n02099601_3004.jpg',
            'https://images.dog.ceo/breeds/retriever-golden/n02099601_5261.jpg',
            'https://images.dog.ceo/breeds/retriever-golden/n02099601_7771.jpg',
            'https://images.dog.ceo/breeds/retriever-golden/n02099601_3120.jpg',
            'https://images.dog.ceo/breeds/retriever-golden/n02099601_2194.jpg',
            'https://images.dog.ceo/breeds/retriever-golden/n02099601_1273.jpg',
        ]

        golden_retrievers = Pet.objects.filter(breed__icontains='Golden Retriever')

        for pet in golden_retrievers:
            self.stdout.write(f'\nAdding photos for {pet.name}...')

            # Use different set of 3 images for each dog
            if pet.name == 'Charlie':
                urls_to_use = golden_urls[0:3]
            elif pet.name == 'Luna':
                urls_to_use = golden_urls[3:6]
            else:
                urls_to_use = golden_urls[0:3]

            for i, url in enumerate(urls_to_use):
                try:
                    self.stdout.write(f'  Downloading photo {i+1} from {url[:50]}...')
                    response = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})

                    if response.status_code == 200:
                        filename = f'{pet.name.lower()}_{i+1}.jpg'
                        photo_field = f'photo{i+1}'
                        field = getattr(pet, photo_field)

                        # Delete old if exists
                        if field:
                            field.delete(save=False)

                        # Save new
                        field.save(filename, ContentFile(response.content), save=False)
                        self.stdout.write(self.style.SUCCESS(f'    ✓ Photo {i+1} saved ({len(response.content)} bytes)'))
                        time.sleep(1)  # Be nice to the API
                    else:
                        self.stdout.write(self.style.WARNING(f'    HTTP {response.status_code}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'    Failed: {e}'))

            pet.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Completed {pet.name}'))

        self.stdout.write(self.style.SUCCESS('\n\n✅ Golden Retriever photos added!'))
