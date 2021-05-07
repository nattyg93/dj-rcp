"""Project wide filters."""
from django_filters import rest_framework as filters


class ChoiceInFilter(filters.BaseInFilter, filters.ChoiceFilter):
    """Validated choice in filter."""


class ModelChoiceInFilter(filters.BaseInFilter, filters.ModelChoiceFilter):
    """Validated model choice in filter."""
