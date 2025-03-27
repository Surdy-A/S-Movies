from django.utils import timezone
from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class User(AbstractUser):
    firstName = models.CharField(max_length=250)
    lastName = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    agree = models.BooleanField(default=False)
    email = models.EmailField(help_text="enter your correct email")
    dateJoined = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="img")
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(1920, 1281)],
                                     format='JPEG',
                                     options={'quality': 95})

    def __str__(self):
        return self.username
        

