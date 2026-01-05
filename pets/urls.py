from django.urls import path
from . import views
from .views_admin import setup_initial_data

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_pets, name='search_pets'),

    # Pet management
    path('pet/add/', views.add_pet, name='add_pet'),
    path('pet/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('pet/<int:pk>/edit/', views.edit_pet, name='edit_pet'),

    # Vaccination
    path('pet/<int:pet_pk>/vaccination/add/', views.add_vaccination, name='add_vaccination'),

    # Matches
    path('pet/<int:pet_pk>/match/', views.send_match_request, name='send_match_request'),
    path('matches/', views.my_matches, name='my_matches'),
    path('match/<int:match_pk>/<str:action>/', views.respond_to_match, name='respond_to_match'),

    # Favorites
    path('pet/<int:pet_pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites, name='favorites'),

    # Admin utility - one-time setup
    path('setup-data/', setup_initial_data, name='setup_data'),
]
