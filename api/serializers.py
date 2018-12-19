from artworks.models import Place, Gender, Artist, ArtistRole, \
        Artwork, Subject, ArtworkSubject
from rest_framework import response, serializers, status


class PlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place
        fields = ('place_id', 'place_name')


class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = ('gender_id', 'gender_name')

class ArtistRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtistRole
        fields = ('artist_role_id', 'artist_role_name')

class ArtistSerializer(serializers.ModelSerializer):
    gender = GenderSerializer(many=False, read_only=True)
    birth_place = PlaceSerializer(many=False, read_only=True)
    death_place = PlaceSerializer(many=False, read_only=True)

    class Meta:
        model = Artist
        fields = ('artist_id', 'artist_name', 'gender', 'birth_place', 'death_place', 'birth_year', 'death_year')

class GrandparentSubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = (
            'subject_id',
            'original_id',
            'subject_name')

class ParentSubjectSerializer(serializers.ModelSerializer):
    parent_subject = GrandparentSubjectSerializer(many=False, read_only=True)

    class Meta:
        model = Subject
        fields = (
            'subject_id',
            'original_id',
            'subject_name')

class SubjectSerializer(serializers.ModelSerializer):
    parent_subject = ParentSubjectSerializer(many=False, read_only=True)

    class Meta:
        model = Subject
        fields = (
            'subject_id',
            'original_id',
            'subject_name',			
            'parent_subject')

class ArtworkSubjectSerializer(serializers.ModelSerializer):
    artwork_id = serializers.ReadOnlyField(source='artwork.artwork_id')
    subject_id = serializers.ReadOnlyField(source='subject.subject_id')

    class Meta:
        model = ArtworkSubject
        fields = ('artwork_id', 'subject_id')


class ArtworkSerializer(serializers.ModelSerializer):
    artwork_name = serializers.CharField(
        allow_blank=False,
        max_length=999
    )
    accession_number = serializers.CharField(
        allow_blank=False,
        max_length=6
    )
    date_text = serializers.CharField(
        allow_blank=True
    )
    medium = serializers.CharField(
        allow_null=True
    )
    credit_line = serializers.CharField(
        allow_null=True
    )
    acquisition_year = serializers.IntegerField(
        allow_null=False
    )
    width = serializers.IntegerField(
        allow_null=True,
    )
    height = serializers.IntegerField(
        allow_null=True,
    )
    depth = serializers.IntegerField(
        allow_null=True,
    )
    artist = ArtistSerializer(
        many=False,
        read_only=True
    )
    artist_id = serializers.PrimaryKeyRelatedField(
        allow_null=False,
        many=False,
        write_only=True,
        queryset=Artist.objects.all(),
        source='artist'
    )
    artist_role = ArtistRoleSerializer(
        many=False,
        read_only=True
    )
    artist_role_id = serializers.PrimaryKeyRelatedField(
        allow_null=False,
        many=False,
        write_only=True,
        queryset=ArtistRole.objects.all(),
        source='artist_role'
    )
    artwork_subject = ArtworkSubjectSerializer(
        source='artwork_subject_set', # Note use of _set
        many=True,
        read_only=True
    )
    subject_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Subject.objects.all(),
        source='artwork_subject'
    )

    class Meta:
        model = Artwork
        fields = (
            'artwork_id',
            'artwork_name',
            'accession_number',
            'date_text',
            'medium',
            'credit_line',
            'acquisition_year',
            'width',
            'height',
            'depth',
            'artist',
            'artist_id',
            'artist_role',
            'artist_role_id',
            'artwork_subject',
            'subject_ids'
        )

    def create(self, validated_data):
        """
        :param validated_data:
        :return: artwork
        """

        # print(validated_data)

        subjects = validated_data.pop('artwork_subject')
        artwork = Artwork.objects.create(**validated_data)

        if subjects is not None:
            for subject in subjects:
                ArtworkSubject.objects.create(
                    artwork_id=artwork.artwork_id,
                    subject_id=subject.subject_id
                )
        return artwork

    def update(self, instance, validated_data):
        artwork_id = instance.artwork_id
        new_subjects = validated_data.pop('artwork_subject')

        instance.artwork_name = validated_data.get(
            'artwork_name',
            instance.artwork_name
        )
        instance.accession_number = validated_data.get(
            'accession_number',
            instance.accession_number
        )
        instance.date_text = validated_data.get(
            'date_text',
            instance.date_text
        )
        instance.medium = validated_data.get(
            'medium',
            instance.medium
        )
        instance.credit_line = validated_data.get(
            'credit_line',
            instance.credit_line
        )
        instance.acquisition_year = validated_data.get(
            'acquisition_year',
            instance.acquisition_year
        )
        instance.width = validated_data.get(
            'width',
            instance.width
        )
        instance.height = validated_data.get(
            'height',
            instance.height
        )
        instance.depth = validated_data.get(
            'depth',
            instance.depth
        )
        instance.artist_id = validated_data.get(
            'artist',
            instance.artist_id
        ).artist_id
        instance.artist_role_id = validated_data.get(
            'artist_role',
            instance.artist_role_id
        ).artist_role_id
        instance.save()

        # If any existing subjects are not in updated list, delete them
        new_ids = []
        old_ids = ArtworkSubject.objects \
            .values_list('subject_id', flat=True) \
            .filter(artwork_id__exact=artwork_id)

        # TODO Insert may not be required (Just return instance)

        # Insert new unmatched subject entries
        for subject in new_subjects:
            new_id = subject.subject_id
            new_ids.append(new_id)
            if new_id in old_ids:
                continue
            else:
                ArtworkSubject.objects \
                    .create(artwork_id=artwork_id, subject_id=new_id)

        # Delete old unmatched subject entries
        for old_id in old_ids:
            if old_id in new_ids:
                continue
            else:
                ArtworkSubject.objects \
                    .filter(artwork_id=artwork_id, subject_id=old_id) \
                    .delete()

        return instance