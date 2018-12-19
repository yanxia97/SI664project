# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.urls import reverse


class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    artist_name = models.CharField(max_length=100)
    gender = models.ForeignKey('Gender', models.DO_NOTHING, blank=True, null=True)
    birth_place = models.ForeignKey('Place', related_name='birth_place', blank=True, null=True, on_delete=models.PROTECT)
    death_place = models.ForeignKey('Place', related_name='death_place', blank=True, null=True, on_delete=models.PROTECT)
    birth_year = models.IntegerField(blank=True, null=True)
    death_year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artist'
        ordering = ['artist_name']
        verbose_name = 'Gallery Artist'
        verbose_name_plural = 'Gallery Artists'

    def __str__(self):
        return self.artist_name

    def get_absolute_url(self):
        # return reverse('artist_detail', args=[str(self.id)])
        return reverse('artist_detail', kwargs={'pk': self.pk})


# class Artist(models.Model):
#     artist_id = models.AutoField(primary_key=True)
#     artist_name = models.CharField(max_length=100)
#     gender = models.ForeignKey('Gender', models.DO_NOTHING, blank=True, null=True)
#     birth_place = models.ForeignKey('Place', models.DO_NOTHING, blank=True, null=True)
#     death_place = models.ForeignKey('Place', models.DO_NOTHING, blank=True, null=True)
#     birth_year = models.IntegerField(blank=True, null=True)
#     death_year = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'artist'

class ArtistRole(models.Model):
    artist_role_id = models.AutoField(primary_key=True)
    artist_role_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'artist_role'
        ordering = ['artist_role_name']
        verbose_name = 'Artist Role in Artworks'
        verbose_name_plural = 'Artist Roles in Artworks'

    def __str__(self):
        return self.artist_role_name

    def get_absolute_url(self):
        # return reverse('artist_detail', args=[str(self.id)])
        return reverse('artist_detail', kwargs={'pk': self.pk})

# class ArtistRole(models.Model):
#     artist_role_id = models.AutoField(primary_key=True)
#     artist_role_name = models.CharField(unique=True, max_length=45)

#     class Meta:
#         managed = False
#         db_table = 'artist_role'


class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    original_id = models.IntegerField()
    subject_name = models.CharField(max_length=45)
    parent_subject = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subject'
        ordering = ['subject_name']
        verbose_name = 'Subject Shown in Artworks'
        verbose_name_plural = 'Subject Shown in Artworks'

    def __str__(self):
        return self.subject_name

    def get_absolute_url(self):
        # return reverse('artwork_detail', args=[str(self.id)])
        return reverse('artwork_detail', kwargs={'pk': self.pk})

# class Subject(models.Model):
#     subject_id = models.AutoField(primary_key=True)
#     original_id = models.IntegerField()
#     subject_name = models.CharField(max_length=45)
#     parent_subject = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'subject'


class Artwork(models.Model):
    artwork_id = models.AutoField(primary_key=True)
    artwork_name = models.CharField(max_length=999)
    accession_number = models.CharField(max_length=6)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)
    artist_role = models.ForeignKey(ArtistRole, on_delete=models.PROTECT)
    date_text = models.CharField(max_length=100)
    medium = models.CharField(max_length=100)
    credit_line = models.CharField(max_length=999)
    acquisition_year = models.IntegerField()
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    depth = models.IntegerField(blank=True, null=True)

    subject = models.ManyToManyField(Subject, through='ArtworkSubject')

    class Meta:
        managed = False
        db_table = 'artwork'
        ordering = ['accession_number']
        verbose_name = 'Gallery Artwork'
        verbose_name_plural = 'Gallery Artworks'

    def __str__(self):
        return self.artwork_name

    def get_absolute_url(self):
        # return reverse('artwork_detail', args=[str(self.id)])
        return reverse('artwork_detail', kwargs={'pk': self.pk})

    @property
    def subject_names(self):
        """
        Returns a list of subjects (names only) associated with an Artwork.
        Note that not all are associated with an Artwork. 
        In such cases the Queryset will return as <QuerySet [None]> and the
        list will need to be checked for None or a TypeError (sequence item 0: expected str
        instance, NoneType found) runtime error will be thrown.
        :return: string
        """
        subjects = self.subject.select_related('parent_subject').order_by('subject_name')

        names = []
        for subject in subjects:
            name = subject.subject_name
            if name is None:
                continue

            if name not in names:
               names.append(name)

        return ', '.join(names)

    @property
    def parent_subject_names(self):
        """
        Returns a list of subjects (names only) associated with an Artwork.
        Note that not all are associated with an Artwork. 
        In such cases the Queryset will return as <QuerySet [None]> and the
        list will need to be checked for None or a TypeError (sequence item 0: expected str
        instance, NoneType found) runtime error will be thrown.
        :return: string
        """
        subjects = self.subject.select_related('parent_subject__parent_subject').order_by('parent_subject__subject_name')

        names = []
        for subject in subjects:
            if (subject.parent_subject):
                name = subject.parent_subject.subject_name
                if name is None:
                    continue

                if name not in names:
                    names.append(name)

        return ', '.join(names)

    @property
    def grandparent_subject_names(self):
        """
        Returns a list of subjects (names only) associated with an Artwork.
        Note that not all are associated with an Artwork.
        In such cases the Queryset will return as <QuerySet [None]> and the
        list will need to be checked for None or a TypeError (sequence item 0: expected str
        instance, NoneType found) runtime error will be thrown.
        :return: string
        """
        subjects = self.subject.select_related('parent_subject__parent_subject').order_by('parent_subject__parent_subject__subject_name')

        names = []
        for subject in subjects:
            if (subject.parent_subject.parent_subject):
                name = subject.parent_subject.parent_subject.subject_name
                if name is None:
                    continue
                    
                if name not in names:
                    names.append(name)

        return ', '.join(names)

    def subject_display(self):
        """Create a string for subject. This is required to display in the Admin view."""
        return ', '.join(
            subject.subject_name for subject in self.subject.all()[:25])

    subject_display.short_description = 'Subjects'

# class Artwork(models.Model):
#     artwork_id = models.AutoField(primary_key=True)
#     artwork_name = models.CharField(max_length=999)
#     accession_number = models.CharField(max_length=6)
#     artist = models.ForeignKey(Artist, models.DO_NOTHING)
#     artist_role = models.ForeignKey(ArtistRole, models.DO_NOTHING)
#     date_text = models.CharField(max_length=100)
#     medium = models.CharField(max_length=100)
#     credit_line = models.CharField(max_length=999)
#     acquisition_year = models.IntegerField()
#     width = models.IntegerField(blank=True, null=True)
#     height = models.IntegerField(blank=True, null=True)
#     depth = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'artwork'


class ArtworkSubject(models.Model):
    artwork_subject_id = models.AutoField(primary_key=True)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'artwork_subject'
        ordering = ['artwork', 'subject']
        verbose_name = 'Gallery Artwork Subject'
        verbose_name_plural = 'Gallery Artwork Subjects'

# class ArtworkSubject(models.Model):
#     artwork_subject_id = models.AutoField(primary_key=True)
#     artwork = models.ForeignKey(Artwork, models.DO_NOTHING)
#     subject = models.ForeignKey('Subject', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'artwork_subject'


class Gender(models.Model):
    gender_id = models.AutoField(primary_key=True)
    gender_name = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'gender'
        ordering = ['gender_name']
        verbose_name = 'Artist Gender'
        verbose_name_plural = 'Artist Genders'

    def __str__(self):
        return self.gender_name

    def get_absolute_url(self):
        # return reverse('artwork_detail', args=[str(self.id)])
        return reverse('artwork_detail', kwargs={'pk': self.pk})

# class Gender(models.Model):
#     gender_id = models.AutoField(primary_key=True)
#     gender_name = models.CharField(unique=True, max_length=10)

#     class Meta:
#         managed = False
#         db_table = 'gender'


class Place(models.Model):
    place_id = models.AutoField(primary_key=True)
    place_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'place'
        ordering = ['place_name']
        verbose_name = 'Birth and Death place of Artists'
        verbose_name_plural = 'Birth and Death places of Artists'

    def __str__(self):
        return self.place_name

    def get_absolute_url(self):
        # return reverse('artwork_detail', args=[str(self.id)])
        return reverse('artwork_detail', kwargs={'pk': self.pk})

# class Place(models.Model):
#     place_id = models.AutoField(primary_key=True)
#     place_name = models.CharField(unique=True, max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'place'

