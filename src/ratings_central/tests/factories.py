"""Factories for users app."""
from datetime import date

import factory
import factory.fuzzy

from ratings_central import enums, models


class PlayerFactory(factory.django.DjangoModelFactory):
    """Player factory."""

    class Meta:
        """Factory meta information."""

        model = models.Player
        django_get_or_create = ["rc_id"]

    rc_id = factory.fuzzy.FuzzyInteger(low=5000, high=2147483647)
    rating = factory.fuzzy.FuzzyInteger(low=0, high=3500)
    st_dev = factory.fuzzy.FuzzyInteger(low=0, high=999)
    rc_primary_club_id = factory.SelfAttribute("primary_club.rc_id")
    last_played = date(2020, 3, 17)
    world_province = "TAS"
    postal_code = "7000"
    country = enums.Country.AUS
    birth = date(1990, 1, 1)
    gender = enums.Gender.FEMALE
    sport = enums.Sport.TABLE_TENNIS
    usatt_id = 0
    tta_id = 0
    ittf_id = 0
    deceased = False

    class Params:
        """Factory params."""

        primary_club = factory.SubFactory(
            "ratings_central.tests.factories.ClubFactory", rc_id=1
        )


class ClubFactory(factory.django.DjangoModelFactory):
    """Club factory."""

    class Meta:
        """Factory meta information."""

        model = models.Club
        django_get_or_create = ["rc_id"]

    rc_id = factory.fuzzy.FuzzyInteger(low=1, high=2147483647)
    name = "My Club"
    nickname = "MC"
    world_province = "TAS"
    postal_code = "7000"
    country = enums.Country.AUS
    sport = enums.Sport.TABLE_TENNIS
    status = enums.ClubStatus.ACTIVE
