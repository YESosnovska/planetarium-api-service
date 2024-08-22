from django.db.models import F, Count
from django.shortcuts import render
from rest_framework import viewsets

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession
)
from planetarium.serializers import (
    ShowThemeSerializer,
    AstronomyShowSerializer,
    PlanetariumDomeSerializer,
    ShowSessionSerializer, ShowThemeListSerializer, ShowThemeDetailSerializer, AstronomyShowListSerializer,
    AstronomyShowDetailSerializer, ShowSessionListSerializer, ShowSessionDetailSerializer
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.prefetch_related("astronomy_shows")
    serializer_class = ShowThemeSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ShowThemeListSerializer

        if self.action == "retrieve":
            return ShowThemeDetailSerializer

        return ShowThemeSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.prefetch_related("show_themes")
    serializer_class = AstronomyShowSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer

        if self.action == "retrieve":
            return AstronomyShowDetailSerializer

        return AstronomyShowSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = (
        ShowSession.objects.all()
        .prefetch_related("astronomy_show", "planetarium_dome")
        .annotate(
            tickets_available=(
                    F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row")
                    - Count("tickets")
            )
        )
    )
    serializer_class = ShowSessionSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer

        if self.action == "retrieve":
            return ShowSessionDetailSerializer

        return ShowSessionSerializer
