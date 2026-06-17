from django.core.management.base import BaseCommand
from movies.models import Movie, Category
import random

class Command(BaseCommand):
    help = "Seed database with test movies"

    def handle(self, *args, **kwargs):

        # Optional: Delete existing movies
        Movie.objects.all().delete()

        # Categories
        cat_nolly, _ = Category.objects.get_or_create(name="nollywood")
        cat_nolly_s, _ = Category.objects.get_or_create(name="nollywood-series")
        cat_holly, _ = Category.objects.get_or_create(name="hollywood")
        cat_holly_s, _ = Category.objects.get_or_create(name="hollywood-series")
        cat_kor, _ = Category.objects.get_or_create(name="korean")
        cat_for, _ = Category.objects.get_or_create(name="foreign")

        categories = [
            cat_nolly,
            cat_nolly_s,
            cat_holly,
            cat_holly_s,
            cat_kor,
            cat_for,
        ]

        genres = [
            "action",
            "adventure",
            "comedy",
            "drama",
            "romance",
            "thriller",
            "horror",
            "science-fiction",
            "fantasy",
            "crime",
            "mystery",
            "animation",
        ]

        countries = [
            "USA",
            "UK",
            "Nigeria",
            "India",
            "South Korea",
        ]

        languages = [
            "English",
            "French",
            "Hausa",
            "Yoruba",
            "Korean",
        ]

        for i in range(60):

            movie = Movie.objects.create(
                title=f"Test Movie {i + 1}",
                genre=random.choice(genres),
                year=str(random.randint(2000, 2025)),
                country=random.choice(countries),
                language=random.choice(languages),
                subtitles="Yes",
                description=f"This is test movie {i + 1}",
                crew="Test Crew",
                director=f"Director {i + 1}",
                producer=f"Producer {i + 1}",
                rating=round(random.uniform(3.0, 5.0), 1),
                video_path=f"/media/movie_{i + 1}.mp4",
                is_series=random.choice([True, False]),
                image="img/default.jpg",
            )

            movie.categories.add(random.choice(categories))

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully created 60 test movies"
            )
        )
