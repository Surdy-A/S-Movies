import os
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils import timezone
from users.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
import ffmpeg
from urllib.parse import urlparse
import yt_dlp
from django.conf import settings
from django.utils.timezone import now

MOVIE_CHOICES = [
        ("Nolly", "Nollywood"),
        ("Nolly-S", "Nollywood Series"),
        ("Holly", "Hollywood"),
        ("Holly-S", "Hollywood Series"),
        ("FOR", "Foreign"),
        ("KOR", "Korean"),
    ]

class Movie(models.Model):
    title = models.CharField(max_length=250)
    genre = models.CharField(max_length=250)
    year = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    subtitles =models.CharField(max_length=250)
    description =models.CharField(max_length=250, default="")
    crew = models.CharField(max_length=250)
    director = models.CharField(max_length=250)
    producer = models.CharField(max_length=250)
    rating = models.DecimalField(default=4.0, max_digits=5, decimal_places=1)
    video_path = models.CharField(max_length=500)
    categories = models.CharField(choices=MOVIE_CHOICES, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_series = models.BooleanField(default=False) 
    image = models.ImageField(upload_to="img")
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(1920, 1281)],
                                     format='JPEG',
                                     options={'quality': 95})
    
    def get_absolute_url(self):
        return reverse("movies:movie_detail", kwargs={"id": self.id})
    
    def average_rating(self):
        ratings = self.ratings.all()
        return ratings.aggregate(models.Avg('score'))['score__avg'] if ratings else 0

    def __str__(self):
        return str('%s - %s' % (self.title, self.producer))


    def is_url(self):
        """Check if the video_path is an online URL."""
        parsed = urlparse(self.video_path)
        return bool(parsed.scheme and parsed.netloc)

    def get_video_duration(self):
        """Returns the duration of the video in HH:MM:SS format (supports both local files and online URLs)."""
        if not self.video_path:
            return "No video path provided"

        try:
            if self.is_url():
                # Fetch metadata for online video
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(self.video_path, download=False)
                    duration = info.get('duration')
            else:
                # Fetch metadata for local video
                probe = ffmpeg.probe(self.video_path)
                duration = float(probe['format']['duration'])

            # Convert seconds to HH:MM:SS format
            hours, remainder = divmod(duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        except Exception as e:
            return f"Error calculating duration: {str(e)}"

class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating scale 1-5

    class Meta:
        unique_together = ('movie', 'user')  # Prevent duplicate ratings

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.score}"


class Season(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="seasons")
    season_number = models.IntegerField()
    episode_count = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def total_episodes(self):
        return self.episodes.count()  #Count related episodes

class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="episodes")
    episode_number = models.IntegerField()
    title = models.CharField(max_length=250)
    air_date = models.DateField()

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)  # Assuming you have a Movie model
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.FloatField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating})"


class Comment(models.Model):
    # movie_id = models.IntegerField()  # ID of the movie the comment belongs to
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # User who made the comment
    text = models.TextField()  # Comment text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    likes = models.IntegerField(default=0)  # Like count
    dislikes = models.IntegerField(default=0)  # Dislike count
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")  # Ensure 'movie' is used
    # Parent comment for replies
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    # Quoted comment reference
    quoted_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='quotes')


    def is_parent(self):
        """Check if the comment is a parent (has no parent)."""
        return self.parent is None
    
    def __str__(self):
        return f"{self.user.username} - {self.text[:30]}"
