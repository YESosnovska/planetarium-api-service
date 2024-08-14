from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.ManyToManyField(ShowTheme, related_name="astronomy_shows")

    def __str__(self):
        return f"{self.title}, description: {self.description}"


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

