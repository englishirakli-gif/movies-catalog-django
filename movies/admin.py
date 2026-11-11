from django.contrib import admin

from .models import Genre, Director, Movie, Festival


admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(Festival)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "release_year", "age_rating", "is_published"]
    list_filter = ["age_rating", "is_published"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ["title"]}
