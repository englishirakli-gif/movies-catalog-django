from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100)
    birth_year = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    class AgeRating(models.TextChoices):
        G = "G", "ყველასთვის"
        PG = "PG", "მშობლის თანხლებით"
        PG13 = "PG13", "13+"
        R = "R", "18+"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    release_year = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    age_rating = models.CharField(max_length=4, choices=AgeRating.choices, default=AgeRating.G)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    language = models.CharField(max_length=30, default="ქართული")
    poster_url = models.URLField(blank=True)

    class Meta:
        ordering = ["-release_year"]
        verbose_name = "ფილმი"
        verbose_name_plural = "ფილმები"

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Festival(models.Model):
    name = models.CharField(max_length=200, unique=True)
    city = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    is_international = models.BooleanField(default=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return f"{self.name} ({self.city})"
