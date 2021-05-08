"""Filters for ratings_central app."""
from django_filters import rest_framework as filters

from ratings_central import models


class PlayerFilter(filters.FilterSet):
    """FilterSet for players endpoint."""

    class Meta:
        """FilterSet Meta information."""

        model = models.Player
        fields = {
            "rc_id": ["exact"],
            "email": ["exact"],
            "name": ["exact", "icontains"],
            "deceased": ["exact"],
        }


class ClubFilter(filters.FilterSet):
    """FilterSet for clubs endpoint."""

    class Meta:
        """FilterSet Meta information."""

        model = models.Club
        fields = {
            "rc_id": ["exact"],
            "email": ["exact"],
            "name": ["exact", "icontains"],
            "status": ["exact"],
        }
