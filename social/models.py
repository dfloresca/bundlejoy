from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create a post model
class Post(models.Model):
    user = models.ForeignKey(
        User, related_name="posts",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_like",  blank=True)
    post_image = models.ImageField(null=True, blank=True, upload_to="images/")


    #keep track or count of likes
    def number_of_likes(self):
        return self.likes.count()
    

    def __str__(self):
        return(
            f"{self.user}"
            f"{self.title}"
            f"({self.created_at: %Y-%m-%d %H:%M}):"
            f"{self.body}..."
        )
# Create a User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One to one relationship with the User model
    follows = models.ManyToManyField(
        'self', 
        related_name='followed_by',
        symmetrical=False,
        blank=True
        )
    
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    
    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    homepage_link = models.CharField(null=True, blank=True, max_length=50)
    facebook_link = models.CharField(null=True, blank=True, max_length=50)
    instagram_link = models.CharField(null=True, blank=True, max_length=50)
        
    def __str__(self):
        return self.user.username

# Create Profile when New User Signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # Have the user follow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


post_save.connect(create_profile, sender=User)

class Comment(models.Model):
    post =  models.ForeignKey('Post', related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
