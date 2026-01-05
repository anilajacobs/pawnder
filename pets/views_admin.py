"""
Admin utility views for initial setup
"""
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.management import call_command
from pets.models import Pet, User
import io
import sys


@require_http_methods(["GET"])
def setup_initial_data(request):
    """
    One-time setup endpoint to load sample data
    Visit: /setup-data/ to initialize the database
    """

    # Capture output
    output = io.StringIO()

    try:
        output.write("<html><head><title>Pawnder Setup</title></head><body>")
        output.write("<h1>Pawnder Initial Data Setup</h1>")
        output.write("<pre style='background: #f5f5f5; padding: 20px; border-radius: 5px;'>")

        # Check current state
        pet_count = Pet.objects.count()
        user_count = User.objects.filter(username__in=['bella_owner', 'max_owner']).count()

        output.write(f"\n{'='*60}\n")
        output.write(f"Current Database State:\n")
        output.write(f"  - Pets: {pet_count}\n")
        output.write(f"  - Sample Users: {user_count}\n")
        output.write(f"{'='*60}\n\n")

        if pet_count > 0:
            output.write("✅ Data already loaded!\n\n")
            output.write("Pets in database:\n")
            for pet in Pet.objects.all():
                photo_status = "✅ Has photos" if pet.photo1 else "❌ No photos"
                output.write(f"  - {pet.name} ({pet.breed}) - {photo_status}\n")
        else:
            output.write("Loading sample data...\n\n")

            # Redirect stdout to capture management command output
            old_stdout = sys.stdout
            sys.stdout = output

            try:
                # Load sample pets and users
                output.write("[1/2] Creating sample pets and users...\n")
                call_command('populate_sample_data')
                output.write("\n")

                # Download photos
                output.write("[2/2] Downloading pet photos...\n")
                call_command('ensure_all_photos')

            finally:
                sys.stdout = old_stdout

            # Verify
            final_count = Pet.objects.count()
            output.write(f"\n✅ Setup Complete!\n")
            output.write(f"   Created {final_count} pets with photos\n\n")

            output.write("Sample Login Accounts:\n")
            output.write("  - Username: bella_owner | Password: password123\n")
            output.write("  - Username: max_owner | Password: password123\n")
            output.write("  - Username: luna_owner | Password: password123\n")
            output.write("  - Username: charlie_owner | Password: password123\n")

        output.write(f"\n{'='*60}\n")
        output.write("\n✅ Your Pawnder app is ready!\n")
        output.write("\n<a href='/'>← Go to Homepage</a>\n")
        output.write("\n</pre></body></html>")

        return HttpResponse(output.getvalue())

    except Exception as e:
        output.write(f"\n\n❌ ERROR: {str(e)}\n")
        output.write("\n</pre></body></html>")
        return HttpResponse(output.getvalue(), status=500)
