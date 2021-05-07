"""Views for the ratings_central app."""
from rest_framework_json_api import views

from ratings_central import models, serializers


class PlayerView(views.ReadOnlyModelViewSet):
    """players endpoint."""

    queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerSerializer
    ordering = ["pk"]


class ClubView(views.ReadOnlyModelViewSet):
    """clubs endpoint."""

    queryset = models.Club.objects.all()
    serializer_class = serializers.ClubSerializer
    ordering = ["pk"]
