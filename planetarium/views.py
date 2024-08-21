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
    ShowSessionSerializer, ShowThemeListSerializer, ShowThemeDetailSerializer
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


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.prefetch_related("astronomy_show", "planetarium_dome")
    serializer_class = ShowSessionSerializer
