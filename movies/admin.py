from django.contrib import admin
from .models import (
    Movie,
    Rating,
    Season,
    Episode,
    Review,
    Category,
    MoviePhoto,
    Comment
)

# -------------------------
# Rating
# -------------------------
admin.site.register(Rating)

# -------------------------
# Movie Photos Inline
# -------------------------
class MoviePhotoInline(admin.TabularInline):
    model = MoviePhoto
    extra = 1


# -------------------------
# Movie Admin (ONLY ONE)
# -------------------------
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "year",
        "rating",
        "created_at"
    )

    search_fields = (
        "title",
        "year"
    )

    list_filter = (
        "year",
        "rating"
    )

    inlines = [MoviePhotoInline]

    def get_genres(self, obj):
        return ", ".join([g.name for g in obj.genres.all()])

    get_genres.short_description = "Genres"


# -------------------------
# Season Admin
# -------------------------
@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("movie", "season_number", "start_date", "end_date")
    list_filter = ("movie", "season_number")
    search_fields = ("movie__title", "season_number")

    def get_total_episodes(self, obj):
        return obj.episodes.count()

    get_total_episodes.short_description = "Total Episodes"


# -------------------------
# Episode Admin
# -------------------------
@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("season", "episode_number", "title", "air_date")
    list_filter = ("season", "air_date")
    search_fields = ("title", "season__movie__title", "season__season_number")


# -------------------------
# Review Admin
# -------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'movie', 'rating', 'created_at')
    search_fields = ('title', 'user__username', 'movie__title')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)


# -------------------------
# Comment Admin
# -------------------------
admin.site.register(Comment)


# -------------------------
# Category Admin
# -------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)