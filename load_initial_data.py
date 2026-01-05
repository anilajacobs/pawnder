#!/usr/bin/env python
"""
Script to load initial data on first deployment
Run this automatically on Render startup
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawnder_project.production_settings')
django.setup()

from pets.models import Pet, User

print("Checking if initial data needs to be loaded...")

# Check if data already exists
if Pet.objects.count() == 0 and User.objects.filter(username='bella_owner').count() == 0:
    print("Loading initial sample data...")

    # Import management command
    from django.core.management import call_command

    # Load sample data
    call_command('populate_sample_data')
    print("✅ Sample data loaded!")

    # Download photos
    print("Downloading pet photos...")
    call_command('ensure_all_photos')
    print("✅ Photos downloaded!")

else:
    print("✅ Data already exists, skipping...")

print("Done!")
