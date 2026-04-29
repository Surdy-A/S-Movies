from django.core.management.base import BaseCommand
from movies.models import Movie, Category
import random

class Command(BaseCommand):
    help = "Seed database with test movies"

    def handle(self, *args, **kwargs):
        genres = ["Action", "Drama", "Comedy", "Horror", "Sci-Fi"]
        countries = ["USA", "UK", "Nigeria", "India"]
        languages = ["English", "French", "Hausa"]

        cat_nolly, _ = Category.objects.get_or_create(name="Nolly")
        cat_nolly_s, _ = Category.objects.get_or_create(name="Nolly-S")
        cat_holly, _ = Category.objects.get_or_create(name="Holly")
        cat_holly_s, _ = Category.objects.get_or_create(name="Holly-S")
        cat_kor, _ = Category.objects.get_or_create(name="KOR")
        cat_for, _ = Category.objects.get_or_create(name="FOR")


        for i in range(20):
            movie = Movie.objects.create(
    title=f"Test Movie {i+1}",
    genre=random.choice(genres),
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

            movie.categories.add(cat_nolly, cat_holly, cat_kor, cat_for, cat_nolly_s, cat_holly_s)

        self.stdout.write(self.style.SUCCESS("Successfully created 20 test movies"))