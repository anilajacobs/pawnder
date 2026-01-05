# Pawnder - Pet Dating & Mating Platform

A Django-based web application for responsible pet breeding and matchmaking. Connect with other pet owners to find the perfect breeding partner for your furry friends!

## Features

### Core Functionality
- **User Registration & Authentication**: Secure user accounts with profile management
- **Pet Profiles**: Comprehensive pet profiles with detailed information including:
  - Basic info (name, breed, species, gender, age)
  - Physical attributes (weight, height, color)
  - Health records (vaccination status, health issues, neutering status)
  - Multiple photo uploads
  - Location and description
  - Breeding preferences

### Pet Matching System
- **Advanced Search**: Filter pets by species, breed, gender, age, vaccination status, and location
- **Match Requests**: Send and receive breeding match requests between pets
- **Match Management**: Accept or reject incoming match requests
- **Favorites**: Save favorite pets for later viewing
- **Owner Contact**: Access contact information for accepted matches

### Health & Vaccination Tracking
- **Vaccination Records**: Maintain detailed vaccination history for each pet
- **Health Documentation**: Track health issues and medical information
- **Vaccination Certificates**: Upload and store vaccination certificates

### User Experience
- **Responsive Design**: Beautiful, mobile-friendly interface
- **Real-time Notifications**: Django messages for user feedback
- **Photo Galleries**: Multiple photos per pet profile
- **Owner Profiles**: Detailed owner information and contact details

## Technology Stack

- **Backend**: Django 5.0
- **Database**: SQLite (development) - easily upgradeable to PostgreSQL/MySQL
- **Frontend**: HTML5, CSS3 (custom styling)
- **Image Handling**: Pillow
- **Authentication**: Django built-in authentication system

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Step 1: Clone or Navigate to Project Directory
```bash
cd /Users/anilajacob/Documents/pawnder
```

### Step 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
The database has already been set up, but if you need to reset it:
```bash
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Step 6: Run Development Server
```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

## Usage Guide

### For Pet Owners

1. **Register an Account**
   - Click "Register" in the navigation
   - Fill in your details (username, email, password)
   - Complete your profile with contact information

2. **Add Your Pet**
   - Click "Add Pet" in the navigation
   - Fill in all required information:
     - Basic details (name, breed, species, gender, date of birth)
     - Physical attributes (weight, height)
     - Health information (vaccination status, health issues)
     - Upload up to 3 photos
     - Add a description highlighting your pet's personality
   - Set breeding preferences

3. **Add Vaccination Records**
   - From your pet's detail page, click "Add Vaccination"
   - Enter vaccine details, dates, and veterinarian information
   - Upload vaccination certificates

4. **Find Matches**
   - Click "Find Matches" to browse available pets
   - Use filters to narrow down search:
     - Species (Dog, Cat, Bird, Rabbit, Other)
     - Breed (e.g., "Shih Tzu")
     - Gender (Male/Female)
     - Age range
     - Location
     - Vaccination status
   - Click on any pet to view full profile

5. **Send Match Requests**
   - From a pet's detail page, click "Send Match Request"
   - Select which of your pets you want to match
   - Write a personalized message introducing your pet
   - Submit the request

6. **Manage Matches**
   - Click "My Matches" to view all match requests
   - **Received Requests**: Accept or reject requests from other owners
   - **Sent Requests**: Track status of your sent requests
   - **Accepted Matches**: View contact information to arrange meetings

7. **Save Favorites**
   - Click the "Add to Favorites" button on any pet profile
   - Access your favorites anytime from "Favorites" in the navigation

### Example Workflow: Finding a Shih Tzu Match

1. **Add Your Pet**
   - Name: Bella
   - Breed: Shih Tzu
   - Gender: Female
   - Age: 2 years
   - Weight: 5.5 kg
   - Upload photos
   - Mark as "Available for Mating"
   - Preferred Breed: Shih Tzu

2. **Search for Matches**
   - Go to "Find Matches"
   - Filter by:
     - Species: Dog
     - Breed: Shih Tzu
     - Gender: Male
     - Vaccinated Only: ✓
   - Browse results

3. **Review Profiles**
   - Check vaccination records
   - Review health information
   - Verify age and weight compatibility
   - Read pet descriptions

4. **Send Match Request**
   - Select matching pet
   - Write message: "Hi! I have a healthy 2-year-old female Shih Tzu named Bella. She's fully vaccinated and has a great temperament. Would love to discuss a potential match!"
   - Submit request

5. **Wait for Response**
   - Monitor "My Matches" for responses
   - Once accepted, contact information will be available

## Admin Panel

Access the Django admin panel at **http://127.0.0.1:8000/admin/**

### Admin Features:
- Manage users and owner profiles
- View and moderate pet listings
- Monitor match requests
- Manage vaccination records
- Access to all system data

## Database Models

### User (Django built-in)
- Username, email, password
- First name, last name

### OwnerProfile
- Extended user information
- Phone, address, city, state, zipcode
- Profile picture
- Linked to User (one-to-one)

### Pet
- Owner (foreign key to User)
- Basic info: name, species, breed, gender, date of birth
- Physical: weight, height, color
- Health: vaccination status, health issues, neutering
- Breeding: availability, preferred breed
- Photos (up to 3)
- Location, description
- Timestamps

### Vaccination
- Linked to Pet
- Vaccine type, name
- Dates: administered, next due
- Veterinarian/clinic information
- Certificate upload
- Notes

### Match
- From pet, to pet (foreign keys)
- Status: Pending, Accepted, Rejected, Cancelled
- Message from requester
- Timestamps

### Favorite
- User, Pet (foreign keys)
- Timestamp

## Project Structure

```
pawnder/
├── pawnder_project/          # Project settings
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── pets/                     # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Django forms
│   ├── urls.py              # App URL patterns
│   ├── admin.py             # Admin configuration
│   ├── templates/pets/      # HTML templates
│   │   ├── base.html        # Base template
│   │   ├── home.html        # Homepage
│   │   ├── search.html      # Pet search
│   │   ├── pet_detail.html  # Pet profile
│   │   ├── profile.html     # User profile
│   │   ├── my_matches.html  # Match management
│   │   └── ...              # Other templates
│   └── migrations/          # Database migrations
├── media/                    # User uploaded files
│   ├── pet_photos/          # Pet photos
│   ├── owner_profiles/      # Owner profile pictures
│   └── vaccination_certificates/  # Vaccination docs
├── venv/                     # Virtual environment
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Security Considerations

- User authentication required for match requests and profile management
- CSRF protection enabled on all forms
- Secure password hashing
- User-specific data access controls
- File upload validation for images and documents

## Future Enhancements

- Email notifications for match requests
- Real-time messaging between matched owners
- Advanced matching algorithm based on compatibility
- Payment integration for premium features
- Veterinarian verification system
- Reviews and ratings for breeding experiences
- Social sharing features
- Mobile app version

## Troubleshooting

### Images not displaying
- Ensure `MEDIA_URL` and `MEDIA_ROOT` are configured in settings.py
- Check that uploaded files are in the `media/` directory
- Verify file permissions

### Database errors
```bash
# Reset database (WARNING: Deletes all data)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Port already in use
```bash
# Use a different port
python manage.py runserver 8001
```

## Support

For issues or questions:
1. Check the Django documentation: https://docs.djangoproject.com/
2. Review error messages in the terminal
3. Check Django debug page (when DEBUG=True)

## License

This project is created for educational and personal use.

## Credits

Developed with Django framework
- Django: https://www.djangoproject.com/
- Python: https://www.python.org/
- Pillow: https://python-pillow.org/

---

Happy matching! Find the perfect partner for your pet with Pawnder! 🐾
