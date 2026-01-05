from django.core.management.base import BaseCommand
from pets.models import Pet
from django.core.files.base import ContentFile
import requests
import time


class Command(BaseCommand):
    help = 'Use stable image URLs that persist on Render'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up stable images for all pets...\n')

        # Stable, reliable image URLs from public sources
        stable_images = {
            'shihtzu': [
                'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=600',  # Shih Tzu 1
                'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600',  # Shih Tzu 2
                'https://images.unsplash.com/photo-1583511655826-05700d3ffd8e?w=600',  # Shih Tzu 3
            ],
            'golden': [
                'https://images.unsplash.com/photo-1633722715463-d30f4f325e24?w=600',  # Golden 1
                'https://images.unsplash.com/photo-1614941907813-e5c2e6d15e5f?w=600',  # Golden 2
                'https://images.unsplash.com/photo-1615751072497-5f5169febe17?w=600',  # Golden 3
            ],
            'persian': [
                'https://images.unsplash.com/photo-1495360010541-f48722b34f7d?w=600',  # Persian cat 1
                'https://images.unsplash.com/photo-1573865526739-10c1dd4e0e7d?w=600',  # Persian cat 2
                'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=600',  # Persian cat 3
            ],
        }

        pets = Pet.objects.all()

        for pet in pets:
            self.stdout.write(f'\nProcessing {pet.name} ({pet.breed})...')

            # Determine which image set to use
            breed_lower = pet.breed.lower()
            if 'shih' in breed_lower or 'shihtzu' in breed_lower:
                urls = stable_images['shihtzu']
            elif 'golden' in breed_lower or 'retriever' in breed_lower:
                urls = stable_images['golden']
            elif 'persian' in breed_lower:
                urls = stable_images['persian']
            else:
                # Generic dog/cat
                urls = stable_images['golden'] if pet.species == 'DOG' else stable_images['persian']

            # Download and save each photo
            for idx, url in enumerate(urls):
                photo_field = f'photo{idx + 1}'

                try:
                    self.stdout.write(f'  Downloading photo {idx + 1}...')

                    # Add timeout and headers
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    response = requests.get(url, timeout=15, headers=headers)

                    if response.status_code == 200:
                        filename = f'{pet.name.lower().replace(" ", "_")}_{idx + 1}.jpg'
                        field = getattr(pet, photo_field)

                        # Delete old photo if exists
                        if field:
                            try:
                                field.delete(save=False)
                            except:
                                pass

                        # Save new photo
                        field.save(filename, ContentFile(response.content), save=False)
                        self.stdout.write(self.style.SUCCESS(f'    ✓ Photo {idx + 1} saved ({len(response.content)} bytes)'))
                        time.sleep(0.5)  # Be nice to the API
                    else:
                        self.stdout.write(self.style.WARNING(f'    HTTP {response.status_code}'))

                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'    Failed: {e}'))

            pet.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Completed {pet.name}'))

        self.stdout.write(self.style.SUCCESS('\n\n✅ All pets now have stable images!'))
        self.stdout.write('\nNote: Images are from Unsplash (free to use)')
