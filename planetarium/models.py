import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from planetarium_service import settings


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def astronomy_show_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/astronomy_shows/", filename)


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(
        null=False,
        blank=False,
        default="add description"
    )
    show_themes = models.ManyToManyField(
        ShowTheme,
        related_name="astronomy_shows"
    )
    image = models.ImageField(null=True, upload_to=astronomy_show_image_file_path)

    def __str__(self):
        return f"{self.title}, description: {self.description}"

    class Meta:
        ordering = ["title"]


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name}: {self.capacity}"


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        AstronomyShow,
        related_name="sessions",
        on_delete=models.CASCADE
    )
    planetarium_dome = models.ForeignKey(
        PlanetariumDome,
        related_name="sessions",
        on_delete=models.DO_NOTHING
    )
    show_time = models.DateTimeField()

    def __str__(self):
        return (f"{self.astronomy_show.title}, "
                f"{self.planetarium_dome.name}, "
                f"{self.show_time}")


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(
        ShowSession,
        related_name="tickets",
        on_delete=models.CASCADE
    )
    reservation = models.ForeignKey(
        Reservation,
        related_name="tickets",
        on_delete=models.CASCADE
    )

    @staticmethod
    def validate_ticket(row, seat, planetarium_dome, error_to_raise):
        for ticket_attr_value, ticket_attr_name, cinema_hall_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(planetarium_dome, cinema_hall_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {cinema_hall_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.show_session.planetarium_dome,
            ValidationError,
        )

    def __str__(self):
        return f"{str(self.show_session)} ({self.row}, {self.seat})"

    class Meta:
        unique_together = ("show_session", "row", "seat")
        ordering = ["row", "seat"]

