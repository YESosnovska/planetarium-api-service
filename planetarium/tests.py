from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium.models import AstronomyShow, ShowTheme
from planetarium.serializers import AstronomyShowListSerializer, AstronomyShowDetailSerializer

ASTRONOMY_SHOW_URL = reverse("planetarium:astronomy-show-list")


def detail_url(astronomy_id):
    return reverse("planetarium:astronomy-show-detail", args=[astronomy_id])


def sample_astronomy_show(**params) -> AstronomyShow:
    defaults = {
        "title": "test",
        "description": "test",
    }
    defaults.update(params)
    return AstronomyShow.objects.create(**defaults)


class UnauthenticatedAstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ASTRONOMY_SHOW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedMovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
        )
        self.client.force_authenticate(user=self.user)

    def test_movie_list(self):
        sample_astronomy_show()

        res = self.client.get(ASTRONOMY_SHOW_URL)
        astronomy_shows = AstronomyShow.objects.all()
        serializer = AstronomyShowListSerializer(astronomy_shows, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_movies_by_title(self):
        show_1 = sample_astronomy_show()
        show_2 = sample_astronomy_show(title="wow")

        res = self.client.get(
            ASTRONOMY_SHOW_URL,
            {"title": show_2.title},
        )

        show_1_serializer = AstronomyShowListSerializer(show_1)
        show_2_serializer = AstronomyShowListSerializer(show_2)

        self.assertIn(show_2_serializer.data, res.data)
        self.assertNotIn(show_1_serializer.data, res.data)

    def test_filter_movies_by_actors(self):
        show_1 = sample_astronomy_show()
        show_2 = sample_astronomy_show(title="wow")

        theme_1 = ShowTheme.objects.create(name="1")
        theme_2 = ShowTheme.objects.create(name="2")

        show_1.show_themes.add(theme_1)
        show_2.show_themes.add(theme_2)

        res = self.client.get(
            ASTRONOMY_SHOW_URL,
            {"show_themes": theme_1.id}
        )

        show_1_serializer = AstronomyShowListSerializer(show_1)
        show_2_serializer = AstronomyShowListSerializer(show_2)

        self.assertIn(show_1_serializer.data, res.data)
        self.assertNotIn(show_2_serializer.data, res.data)

    def test_retrieve_movie_detail(self):
        show = sample_astronomy_show()
        theme = ShowTheme.objects.create(name="Drama")

        show.show_themes.add(theme)

        url = detail_url(show.id)

        res = self.client.get(url)

        serializer = AstronomyShowDetailSerializer(show)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_movie_forbidden(self):
        payload = {
            "title": "test",
            "description": "test",
        }

        res = self.client.post(
            ASTRONOMY_SHOW_URL,
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
