from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# To handle each post.
class Posts(models.Model):
    name = models.CharField(max_length=200, default='user')
    post = models.TextField(max_length=None)
    likes = models.IntegerField(max_length=None, default=0)
    date = models.DateTimeField()
    state = models.CharField(max_length=200, default='up')
    liked_by = models.CharField(max_length=200, default='')

    def serialize(self):
        return{
            "id":self.id,
            "name": self.name,
            "post": self.post,
            "likes": self.likes,
            "date": self.date.strftime("%b %d %Y, %I:%M %p")
        }

    def __str__(self):
        return self.name


# Model to handle details of each post.
class UserDetails(models.Model):

    name = models.CharField(max_length=200, default='name')
    followers = models.CharField(max_length=200, default='names')
    following = models.CharField(max_length=200, default='names')

    def serialize(self):
        return{
            "name": self.name,
            "followers": self.followers,
            "following": self.following
        }

    def __str__(self):
        return self.name


# Model to handle likes and unlikes of a post.
class Likes(models.Model):

    liked_post = models.ForeignKey(Posts, models.CASCADE, related_name="liked_post", default='')
    liked_by = models.ForeignKey(User, models.CASCADE, related_name='liked_by', default='')






