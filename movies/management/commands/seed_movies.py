from django.core.management.base import BaseCommand
from movies.models import Movie, Category, Genre
import random


class Command(BaseCommand):
    help = "Seed database with test movies"

    def handle(self, *args, **kwargs):

        # ----------------------------
        # Create Genres
        # ----------------------------
        genre_names = [
            "Action",
            "Adventure",
            "Comedy",
            "Drama",
            "Romance",
            "Thriller",
            "Horror",
            "Science Fiction",
            "Fantasy",
            "Crime",
            "Mystery",
            "Animation"
        ]

        genres = []  # ✅ FIXED: single list only

        for name in genre_names:  # ❌ FIXED: was looping wrong variable

            genre, created = Genre.objects.get_or_create(name=name)

            # ALWAYS update SEO + slug
            genre.slug = name.lower().replace(" ", "-")
            genre.seo_title = f"Best {name} Movies Online | S-Movies"
            genre.seo_description = (
                f"Watch the best {name} movies and series online in HD. "
                f"Stream latest {name} content from Hollywood, Nollywood, Korean and more on S-Movies."
            )

            genre.save()

            genres.append(genre)

        # ----------------------------
        # Categories
        # ----------------------------
        cat_nolly, _ = Category.objects.get_or_create(name="nollywood")
        cat_nolly_s, _ = Category.objects.get_or_create(name="nollywood-series")
        cat_holly, _ = Category.objects.get_or_create(name="hollywood")
        cat_holly_s, _ = Category.objects.get_or_create(name="hollywood-series")
        cat_kor, _ = Category.objects.get_or_create(name="korean")
        cat_for, _ = Category.objects.get_or_create(name="foreign")

        countries = ["USA", "UK", "Nigeria", "India"]
        languages = ["English", "French", "Hausa"]

        # ----------------------------
        # Create Movies
        # ----------------------------
        for i in range(60):

            movie = Movie.objects.create(
                title=f"Test Movie {i+1}",
                year=str(random.randint(2000, 2025)),
                country=random.choice(countries),
                language=random.choice(languages),
                subtitles="Yes",
                description=f"This is test movie {i+1}",
                crew="Test Crew",
                director="Test Director",
                producer="Test Producer",
                rating=round(random.uniform(3.0, 5.0), 1),
                video_path=f"/media/movie_{i+1}.mp4",
                is_series=False,
                image="img/default.jpg"
            )

            # ----------------------------
            # Add Categories
            # ----------------------------
            movie.categories.add(
                cat_nolly,
                cat_holly,
                cat_kor,
                cat_for,
                cat_nolly_s,
                cat_holly_s
            )

            # ----------------------------
            # Add Genres (SAFE VERSION)
            # ----------------------------
            k = random.randint(1, min(3, len(genres)))
            selected_genres = random.sample(genres, k=k)

            movie.genres.set(selected_genres)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully created 60 test movies with genres + SEO"
            )
        )