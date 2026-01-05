from django.contrib import admin
from .models import OwnerProfile, Pet, Vaccination, Match, Favorite


@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'state', 'created_at')
    list_filter = ('city', 'state', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'city')


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'gender', 'species', 'owner', 'age_in_years', 'is_vaccinated', 'is_available_for_mating', 'created_at')
    list_filter = ('species', 'gender', 'breed', 'is_vaccinated', 'is_available_for_mating', 'created_at')
    search_fields = ('name', 'breed', 'owner__username', 'location')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'name', 'species', 'breed', 'gender', 'date_of_birth', 'color')
        }),
        ('Physical Attributes', {
            'fields': ('weight', 'height')
        }),
        ('Health Information', {
            'fields': ('is_vaccinated', 'last_vaccination_date', 'health_issues', 'is_neutered')
        }),
        ('Breeding Preferences', {
            'fields': ('is_available_for_mating', 'preferred_breed')
        }),
        ('Media', {
            'fields': ('photo1', 'photo2', 'photo3')
        }),
        ('Other', {
            'fields': ('location', 'description', 'is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ('pet', 'vaccine_type', 'date_administered', 'next_due_date', 'veterinarian_name')
    list_filter = ('vaccine_type', 'date_administered')
    search_fields = ('pet__name', 'veterinarian_name', 'clinic_name')
    readonly_fields = ('created_at',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('from_pet', 'to_pet', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('from_pet__name', 'to_pet__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'pet__name')
    readonly_fields = ('created_at',)
