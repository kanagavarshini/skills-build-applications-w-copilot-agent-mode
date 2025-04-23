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
    # Enhanced user features
    experience_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    badges = models.JSONField(default=dict)  # Store earned badges/achievements
    weight_history = models.JSONField(default=list)  # Track weight changes over time
    notification_preferences = models.JSONField(default=dict)  # Store notification settings
    personal_records = models.JSONField(default=dict)  # Store best performances
    streak_history = models.JSONField(default=list)  # Track workout streaks
    favorite_workouts = models.JSONField(default=list)  # Store IDs of favorite workouts

    def __str__(self):
        return self.username

class Team(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    members = models.ManyToManyField(User, related_name='teams')
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    # Enhanced team features
    specialty = models.CharField(max_length=50, null=True)
    achievement_points = models.IntegerField(default=0)
    monthly_goal = models.IntegerField(default=1000)
    last_challenge_date = models.DateTimeField(null=True)
    announcements = models.JSONField(default=list)  # Store team announcements
    challenge_history = models.JSONField(default=list)  # Track past challenges
    team_ranking = models.IntegerField(default=0)  # Overall team ranking
    weekly_goals = models.JSONField(default=dict)  # Store weekly targets
    events_calendar = models.JSONField(default=list)  # Upcoming team events
    team_stats = models.JSONField(default=dict)  # Aggregate team statistics

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
    location_data = models.JSONField(null=True)  # GPS coordinates and route
    weather_conditions = models.JSONField(null=True)  # Weather during activity
    heart_rate_data = models.JSONField(null=True)  # Heart rate tracking
    notes = models.TextField(null=True)  # Personal notes
    progress_photos = models.JSONField(default=list)  # Photo URLs
    workout_plan = models.ForeignKey('Workout', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"

class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    # Enhanced leaderboard stats
    total_activities = models.IntegerField(default=0)
    total_duration = models.DurationField(default=timedelta(0))
    total_calories = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_active = models.DateTimeField(default=timezone.now)
    monthly_rankings = models.JSONField(default=list)  # Historical rankings
    achievement_breakdown = models.JSONField(default=dict)  # Points by category
    badges_earned = models.JSONField(default=list)  # List of earned badges
    challenge_participations = models.JSONField(default=list)  # Challenge history

    def __str__(self):
        return f"{self.user.username} - Score: {self.score}"

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    # Enhanced workout details
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
    difficulty_rating = models.FloatField(null=True)
    success_rate = models.IntegerField(null=True)
    prerequisites = models.JSONField(default=list)  # Required skills/equipment
    progression_levels = models.JSONField(default=dict)  # Different difficulty versions
    media_links = models.JSONField(default=dict)  # Videos/images
    coach_notes = models.TextField(null=True)  # Notes for trainers
    substitute_exercises = models.JSONField(default=dict)  # Alternative exercises

    def __str__(self):
        return self.name