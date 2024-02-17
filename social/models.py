from django.db import models
from django.contrib.auth.models import User

# Create a User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One to one relationship with the User model
    follows = models.ManyToManyField(
        'self', 
        related_name='followed_by',
        symmetrical=False,
        blank=True
        )
