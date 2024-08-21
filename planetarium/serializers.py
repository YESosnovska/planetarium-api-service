from rest_framework import serializers

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    ShowSession,
    PlanetariumDome
)


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name", "shows")


class ShowThemeListSerializer(serializers.ModelSerializer):
    shows = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="title"
    )

    class Meta:
        model = ShowTheme
        fields = (
            "id",
            "name",
            "shows"
        )


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_themes")


class AstronomyShowListSerializer(serializers.ModelSerializer):
    themes = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = AstronomyShow
        fields = (
            "id",
            "title",
            "description",
            "themes",
        )


class AstronomyShowDetailSerializer(serializers.ModelSerializer):
    themes = ShowThemeSerializer(many=True, read_only=True)

    class Meta:
        model = AstronomyShow
        fields = (
            "id",
            "title",
            "description",
            "themes"
        )


class ShowThemeDetailSerializer(serializers.ModelSerializer):
    shows = AstronomyShowSerializer(many=True, read_only=True)

    class Meta:
        model = ShowTheme
        fields = (
            "id",
            "name",
            "shows"
        )


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row")


class ShowSessionSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.CharField(
        source="astronomy_show.title",
        read_only=True
    )
    planetarium_dome = serializers.CharField(
        source="planetarium_dome.title",
        read_only=True
    )

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")
