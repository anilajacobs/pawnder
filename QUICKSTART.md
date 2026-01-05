# Pawnder - Quick Start Guide

Get your pet dating platform running in 5 minutes!

## Quick Setup (Already Done!)

The project is already set up and ready to run. The database has been migrated and all dependencies are installed.

## Start the Server

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

3. **Open your browser and visit:**
   ```
   http://127.0.0.1:8000/
   ```

## First Steps

### Create an Admin Account
```bash
python manage.py createsuperuser
```

You'll be prompted for:
- Username
- Email
- Password

### Access Admin Panel
Visit: http://127.0.0.1:8000/admin/

Login with your superuser credentials.

### Try the Application

1. **Register as a User**
   - Go to http://127.0.0.1:8000/
   - Click "Register"
   - Fill in your details

2. **Add a Pet**
   - Click "Add Pet"
   - Fill in your pet's details:
     - Name: e.g., "Bella"
     - Species: "Dog"
     - Breed: e.g., "Shih Tzu"
     - Gender: "Female"
     - Date of Birth: e.g., "2022-01-15"
     - Weight: e.g., "5.5" kg
     - Upload photos (optional but recommended)
     - Check "Vaccinated" if applicable
     - Check "Available for Mating"

3. **Add Vaccination Records** (Optional)
   - From your pet's profile page
   - Click "Add Vaccination"
   - Fill in vaccine details

4. **Search for Matches**
   - Click "Find Matches"
   - Use filters to search (breed, gender, age, etc.)
   - Browse available pets

5. **Test Match Request**
   - Create a second user account (use incognito/private window)
   - Add a pet with opposite gender, same breed
   - Send a match request between the pets
   - Switch back to first account to accept/reject

## Example Scenario: Shih Tzu Dating

### User 1 (You):
- Username: bella_owner
- Pet: Bella (Female Shih Tzu, 2 years old)
- Weight: 5.5 kg
- Fully vaccinated
- Available for mating

### User 2 (Test Account):
- Username: max_owner
- Pet: Max (Male Shih Tzu, 3 years old)
- Weight: 6.0 kg
- Fully vaccinated
- Available for mating

### Workflow:
1. User 2 searches for Female Shih Tzus
2. Finds Bella's profile
3. Reviews vaccination records and health info
4. Sends match request with message
5. User 1 receives notification
6. User 1 reviews Max's profile
7. User 1 accepts match
8. Both users can now see contact information

## Checking Vaccination Requirements

When viewing a pet's profile, you can:
- See all vaccination records
- Check vaccination dates
- Verify vaccination status (badge shows "Vaccinated")
- View uploaded vaccination certificates
- Check health issues section

## Key Features to Test

✅ User registration and login
✅ Pet profile creation with photos
✅ Vaccination record management
✅ Advanced search with filters
✅ Match request system
✅ Accept/reject match requests
✅ View contact info for accepted matches
✅ Favorites system
✅ Owner profile management

## Project URLs

- **Homepage:** http://127.0.0.1:8000/
- **Login:** http://127.0.0.1:8000/login/
- **Register:** http://127.0.0.1:8000/register/
- **Search Pets:** http://127.0.0.1:8000/search/
- **My Profile:** http://127.0.0.1:8000/profile/
- **My Matches:** http://127.0.0.1:8000/matches/
- **Favorites:** http://127.0.0.1:8000/favorites/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## Stopping the Server

Press `Ctrl + C` in the terminal where the server is running.

## Deactivate Virtual Environment

When you're done:
```bash
deactivate
```

## Need Help?

Check the full README.md for:
- Detailed feature documentation
- Database model explanations
- Troubleshooting guide
- Security information
- Future enhancement ideas

---

Happy pet matchmaking! 🐾
