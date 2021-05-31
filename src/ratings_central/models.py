"""Models for the ratings_central app."""
from django.db import models
from django_cryptography.fields import encrypt

from ratings_central import enums


class Player(models.Model):
    """Ratings Central Player information."""

    rc_id = models.IntegerField(db_index=True)
    rating = models.IntegerField()
    st_dev = models.IntegerField()
    last_played = models.DateField()
    rc_primary_club_id = models.IntegerField()
    name = models.CharField(max_length=50)
    address_one = models.CharField(max_length=50)
    address_two = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    na_state = models.CharField(max_length=2, choices=enums.NorthAmericaState.choices)
    world_province = models.CharField(max_length=25)
    postal_code = models.CharField(max_length=16)
    country = models.CharField(max_length=3, choices=enums.Country.choices)
    email = models.EmailField(max_length=254)
    birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=enums.Gender.choices)
    sport = models.IntegerField(choices=enums.Sport.choices)
    usatt_id = models.IntegerField()
    tta_id = models.IntegerField()
    ittf_id = models.IntegerField()
    deceased = models.BooleanField()

    class JSONAPIMeta:
        """JSON:API meta information."""

        resource_name = "players"


class Club(models.Model):
    """Ratings Central Club information."""

    rc_id = models.IntegerField(db_index=True)
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=15)
    address_one = models.CharField(max_length=50)
    address_two = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    na_state = models.CharField(max_length=2, choices=enums.NorthAmericaState.choices)
    world_province = models.CharField(max_length=25)
    postal_code = models.CharField(max_length=16)
    country = models.CharField(max_length=3, choices=enums.Country.choices)
    email = models.EmailField(max_length=254)
    website = models.CharField(max_length=80)
    phone = models.CharField(max_length=25)
    sport = models.IntegerField(choices=enums.Sport.choices)
    status = models.CharField(max_length=8, choices=enums.ClubStatus.choices)

    class JSONAPIMeta:
        """JSON:API meta information."""

        resource_name = "clubs"


class Director(models.Model):
    """Ratings Central Director information."""

    rc_id = models.IntegerField(db_index=True)
    password = encrypt(models.TextField())
