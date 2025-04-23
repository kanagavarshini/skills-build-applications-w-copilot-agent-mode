# Register models in the admin site
from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'fitness_level', 'fitness_goal', 'created_at')
    list_filter = ('fitness_level', 'fitness_goal', 'preferred_workout_time')
    search_fields = ('username', 'email')
    date_hierarchy = 'created_at'

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'score', 'achievement_points', 'created_at')
    list_filter = ('specialty',)
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    filter_horizontal = ('members',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'intensity', 'duration', 'calories_burned', 'created_at')
    list_filter = ('activity_type', 'intensity')
    search_fields = ('user__username', 'activity_type')
    date_hierarchy = 'created_at'

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'total_activities', 'streak_days', 'last_active')
    list_filter = ('streak_days',)
    search_fields = ('user__username',)
    date_hierarchy = 'last_active'

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'team', 'created_by', 'duration', 'estimated_calories')
    list_filter = ('difficulty', 'team')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'