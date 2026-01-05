#!/usr/bin/env python
"""
Script to load initial data on first deployment
Run this automatically on Render startup
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawnder_project.production_settings')
django.setup()

from pets.models import Pet, User

print("\n" + "="*50)
print("PAWNDER - Initial Data Loader")
print("="*50)

try:
    print("\n[1/3] Checking if initial data needs to be loaded...")

    # Check if data already exists
    pet_count = Pet.objects.count()
    user_count = User.objects.filter(username__in=['bella_owner', 'max_owner', 'luna_owner', 'charlie_owner']).count()

    print(f"Current state: {pet_count} pets, {user_count} sample users")

    if pet_count == 0 or user_count == 0:
        print("\n[2/3] Loading sample data (users, pets, vaccinations)...")

        # Import management command
        from django.core.management import call_command

        try:
            call_command('populate_sample_data')
            print("✅ Sample data loaded successfully!")
        except Exception as e:
            print(f"⚠️ Error loading sample data: {e}")
            print("Continuing anyway...")

        # Download photos - with error handling
        print("\n[3/3] Downloading pet photos from internet...")
        try:
            call_command('ensure_all_photos')
            print("✅ Pet photos downloaded successfully!")
        except Exception as e:
            print(f"⚠️ Warning: Could not download all photos: {e}")
            print("Photos will use placeholders or can be uploaded later via admin panel")

        # Verify final state
        final_pets = Pet.objects.count()
        final_users = User.objects.filter(username__in=['bella_owner', 'max_owner', 'luna_owner', 'charlie_owner']).count()
        print(f"\n✅ Setup complete! Created {final_users} users and {final_pets} pets")

    else:
        print("✅ Data already exists, skipping initial load")

    print("\n" + "="*50)
    print("READY! Your Pawnder app is set up!")
    print("="*50 + "\n")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("App will still start, but without sample data")
    print("You can add data manually via admin panel")
    import traceback
    traceback.print_exc()
    sys.exit(0)  # Don't fail the build
