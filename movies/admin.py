from django.contrib import admin
from .models import Movie, Rating, Season, Episode, Review, Category, MoviePhoto, Comment

# Register your models here.
# admin.site.register(Movie)
admin.site.register(Rating)

class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "year", "rating", "created_at")
    search_fields = ("title", "genre", "year")
    list_filter = ("year", "genre", "rating")

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("movie", "season_number", "start_date", "end_date")
    list_filter = ("movie", "season_number")
    search_fields = ("movie__title", "season_number")

    def get_total_episodes(self, obj):
        return obj.episodes.count()
    get_total_episodes.short_description = "Total Episodes"

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("season", "episode_number", "title", "air_date")
    list_filter = ("season", "air_date")
    search_fields = ("title", "season__movie__title", "season__season_number")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'movie', 'rating', 'created_at')
    search_fields = ('title', 'user__username', 'movie__title')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)


admin.site.register(Comment)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class MoviePhotoInline(admin.TabularInline):
    model = MoviePhoto
    extra = 1

class MovieAdmin(admin.ModelAdmin):
    inlines = [MoviePhotoInline]

admin.site.register(Movie, MovieAdmin)