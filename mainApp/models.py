from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import now
# Create your models here.

class otp(models.Model):
    email = models.CharField(max_length=200)
    otp = models.CharField(max_length=200)

    def __str__(self):
        return self.email

class HomeworkUploads(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()
    date = models.DateField(default=now)
    files = models.FileField(upload_to="uploads")
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    views = models.IntegerField(default=0)
    desc = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Preferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(HomeworkUploads, on_delete=models.CASCADE)
    preference = models.IntegerField(default=0)

class Notifications(models.Model):
    image = models.ImageField(upload_to = "notifications")
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    date = models.DateField(default=now())

    def __str__(self):
        return self.title


class Quotes(models.Model):
    quote = models.CharField(max_length=200)
    writter = models.CharField(max_length=200)
    aurhor = models.ImageField(upload_to='motivation')
    date = models.DateField(default=now())
    color = models.CharField(max_length=200)

class Question(models.Model):
    files = models.FileField(upload_to='questions')
    date = models.DateField(default=now)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Note(models.Model):
    topic = models.CharField(max_length=200)
    date = models.DateField(default=now)
    files = models.FileField(upload_to='notes')
    

    

    
    
    