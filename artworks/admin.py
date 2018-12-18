from django.contrib import admin

import artworks.models as models

@admin.register(models.Artist)
class ArtistAdmin(admin.ModelAdmin):
    fields = [
        'artist_name',
        'gender',
        'birth_place',
        'death_place',
        'birth_year',
        'death_year'
    ]

    list_display = [
        'artist_name',
        'gender',
        'birth_place',
        'death_place',
        'birth_year',
        'death_year'
    ]

    list_filter = ['gender', 'birth_year', 'death_year']

@admin.register(models.ArtistRole)
class ArtistRoleAdmin(admin.ModelAdmin):
    fields = ['artist_role_name']
    list_display = ['artist_role_name']
    ordering = ['artist_role_name']

@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    fields = ['original_id', 'subject_name', 'parent_subject']
    list_display = ['original_id', 'subject_name', 'parent_subject']
    ordering = ['subject_name']

@admin.register(models.Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    fields = [
        'artwork_name',
        'accession_number',
        'artist',
        'artist_role',
        'date_text',
        'medium',
        'credit_line',
        'acquisition_year',
        (
            'width',
            'height',
            'depth'
        )        
    ]

    list_display = [
        'artwork_name',
        'accession_number',
        'artist',
        'artist_role',
        'date_text',
        'medium',
        'acquisition_year',
        'subject_display'
    ]

    list_filter = ['artist_role', 'acquisition_year']

@admin.register(models.Gender)
class GenderAdmin(admin.ModelAdmin):
    fields = ['gender_name']
    list_display = ['gender_name']
    ordering = ['gender_name']

@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    fields = ['place_name']
    list_display = ['place_name']
    ordering = ['place_name']
