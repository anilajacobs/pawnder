from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from pets.models import Pet
import requests
import random


class Command(BaseCommand):
    help = 'Downloads and adds sample photos to pets'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding photos to pets...\n')

        # Sample pet image URLs (using placeholder services with real pet photos)
        dog_images = [
            'https://images.dog.ceo/breeds/shihtzu/n02086240_3139.jpg',
            'https://images.dog.ceo/breeds/shihtzu/n02086240_4615.jpg',
            'https://images.dog.ceo/breeds/shihtzu/n02086240_2894.jpg',
            'https://images.dog.ceo/breeds/retriever-golden/n02099601_3004.jpg',
            'https://images.dog.ceo/breeds/retriever-golden/n02099601_5261.jpg',
            'https://images.dog.ceo/breeds/retriever-golden/n02099601_7771.jpg',
            'https://images.dog.ceo/breeds/retriever-golden/n02099601_3120.jpg',
        ]

        cat_images = [
            'https://cdn2.thecatapi.com/images/MTU0OTkxNQ.jpg',
            'https://cdn2.thecatapi.com/images/71a.jpg',
            'https://cdn2.thecatapi.com/images/5k8.jpg',
        ]

        pets = Pet.objects.all()

        for pet in pets:
            try:
                # Select images based on species
                if pet.species == 'DOG':
                    image_urls = dog_images
                elif pet.species == 'CAT':
                    image_urls = cat_images
                else:
                    continue

                # Download and save up to 3 photos
                for i, photo_field in enumerate(['photo1', 'photo2', 'photo3']):
                    if i < len(image_urls):
                        url = image_urls[i % len(image_urls)]

                        try:
                            response = requests.get(url, timeout=10)
                            if response.status_code == 200:
                                filename = f'{pet.name.lower().replace(" ", "_")}_{i+1}.jpg'
                                getattr(pet, photo_field).save(
                                    filename,
                                    ContentFile(response.content),
                                    save=False
                                )
                                self.stdout.write(f'  Added photo {i+1} to {pet.name}')
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f'  Could not download photo for {pet.name}: {e}'))

                pet.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Updated photos for {pet.name}\n'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {pet.name}: {e}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Finished adding photos to pets!'))
