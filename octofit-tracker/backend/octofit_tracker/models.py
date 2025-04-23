from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    # Profile fields
    fitness_level = models.CharField(max_length=20, default='Beginner')
    fitness_goal = models.CharField(max_length=50, default='General Fitness')
    preferred_workout_time = models.CharField(max_length=20, default='Morning')
    height = models.IntegerField(null=True)  # in cm
    weight = models.FloatField(null=True)    # in kg
    target_weight = models.FloatField(null=True)  # in kg
    team_role = models.CharField(max_length=20, null=True)
    team_join_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.username

class Team(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    members = models.ManyToManyField(User, related_name='teams')
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    # Additional team fields
    specialty = models.CharField(max_length=50, null=True)
    achievement_points = models.IntegerField(default=0)
    monthly_goal = models.IntegerField(default=1000)
    last_challenge_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100, default='general')
    duration = models.DurationField(default=timedelta(minutes=30))
    created_at = models.DateTimeField(default=timezone.now)
    # Enhanced activity tracking
    variation = models.CharField(max_length=100, null=True)
    intensity = models.CharField(max_length=20, null=True)
    calories_burned = models.IntegerField(default=0)
    achievement_points = models.IntegerField(default=0)
    mood_rating = models.IntegerField(null=True)  # 1-5 scale
    perceived_effort = models.IntegerField(null=True)  # 1-10 scale

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"

class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    # Additional statistics
    total_activities = models.IntegerField(default=0)
    total_duration = models.DurationField(default=timedelta(0))
    total_calories = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_active = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - Score: {self.score}"

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    # Workout details
    difficulty = models.CharField(max_length=20, null=True)
    equipment_needed = models.TextField(null=True)
    estimated_calories = models.IntegerField(default=0)
    target_muscles = models.TextField(null=True)
    duration = models.DurationField(default=timedelta(minutes=45))
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    scheduled_time = models.DateTimeField(null=True)
    max_participants = models.IntegerField(default=20)
    current_participants = models.IntegerField(default=0)
    difficulty_rating = models.FloatField(null=True)  # Average user rating
    success_rate = models.IntegerField(null=True)  # Percentage of completions

    def __str__(self):
        return self.name