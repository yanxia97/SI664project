import django_filters
from artworks.models import Artwork, Artist, ArtistRole, Subject


class ArtworkFilter(django_filters.FilterSet):
    artwork_name = django_filters.CharFilter(
        field_name='artwork_name',
        label='Artwork Name',
        lookup_expr='icontains'
    )

    accession_number = django_filters.CharFilter(
        field_name='accession_number',
        label='Accession Number',
        lookup_expr='exact'
    )

    artist = django_filters.ModelChoiceFilter(
        field_name='artist',
        label='Artist',
        queryset=Artist.objects.all().order_by('artist_name'),
        lookup_expr='exact'
    )

    artist_role = django_filters.ModelChoiceFilter(
        field_name='artist_role',
        label='Artist Role',
        queryset=ArtistRole.objects.all().order_by('artist_role_name'),
        lookup_expr='exact'
    )

    date_text = django_filters.CharFilter(
        field_name='date_text',
        label='Date Text',
        lookup_expr='icontains'
    )

    medium = django_filters.CharFilter(
        field_name='medium',
        label='Medium',
        lookup_expr='icontains'
    )

    credit_line = django_filters.CharFilter(
        field_name='credit_line',
        label='Credit Line',
        lookup_expr='icontains'
    )

    acquisition_year = django_filters.NumberFilter(
        field_name='acquisition_year',
        label='Year Acquisited',
        lookup_expr='exact'
    )

    width = django_filters.NumberFilter(
        field_name='width',
        label='Width',
        lookup_expr='exact'
    )

    height = django_filters.NumberFilter(
        field_name='height',
        label='Height',
        lookup_expr='exact'
    )

    wdepthidth = django_filters.NumberFilter(
        field_name='depth',
        label='Depth',
        lookup_expr='exact'
    )

    subject = django_filters.ModelChoiceFilter(
        field_name='subject',
        label='Subject',
        queryset=Subject.objects.all().order_by('subject_name'),
        lookup_expr='exact'
    )

    class Meta:
        model = Artwork
        # form = SearchForm
        # fields [] is required, even if empty.
        fields = []