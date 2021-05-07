"""Serializers for the ratings_central app."""
from rest_framework_json_api import serializers

from ratings_central import models


class PlayerSerializer(serializers.ModelSerializer):
    """Player serializer."""

    class Meta:
        """Serializer meta information."""

        model = models.Player
        read_only_fields = [
            "rc_id",
            "rating",
            "st_dev",
            "last_played",
            "rc_primary_club_id",
            "name",
            "address_one",
            "address_two",
            "city",
            "na_state",
            "world_province",
            "postal_code",
            "country",
            "email",
            "birth",
            "gender",
            "sport",
            "usatt_id",
            "tta_id",
            "ittf_id",
            "deceased",
        ]
        fields = read_only_fields


class ClubSerializer(serializers.ModelSerializer):
    """Club serializer."""

    class Meta:
        """Serializer meta information."""

        model = models.Club
        read_only_fields = [
            "rc_id",
            "name",
            "nickname",
            "address_one",
            "address_two",
            "city",
            "na_state",
            "world_province",
            "postal_code",
            "country",
            "email",
            "website",
            "phone",
            "sport",
            "status",
        ]
        fields = read_only_fields
