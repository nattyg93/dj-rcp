"""Filters for users app."""
from django_filters import rest_framework as filters

from common.filters import ChoiceInFilter
from users import models


class UserFilter(filters.FilterSet):
    """FilterSet for users endpoint."""

    roles__in = ChoiceInFilter(
        field_name="groups__name", lookup_expr="in", choices=models.get_role_choices()
    )

    class Meta:
        """FilterSet Meta information."""

        model = models.User
        fields = {
            "email": ["exact"],
        }
