from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

class Team(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    members = models.JSONField()  # Store as JSON array of usernames
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=100)
    calories_burned = models.IntegerField()
    type = models.CharField(max_length=100)
    average_duration = models.IntegerField()  # Duration in minutes
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Leaderboard(models.Model):
    username = models.CharField(max_length=100)
    score = models.IntegerField()
    rank = models.IntegerField()
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} - Rank {self.rank}"

class Workout(models.Model):
    username = models.CharField(max_length=100)
    activity = models.CharField(max_length=100)
    duration = models.IntegerField()  # Duration in minutes
    calories_burned = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} - {self.activity}"