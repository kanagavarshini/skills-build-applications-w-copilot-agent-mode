from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone, timedelta
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create users
        users = [
            User.objects.create(
                username="thundergod",
                email="thundergod@octofit.edu",
                password=make_password("password123"),
                created_at=datetime.now(timezone.utc)
            ),
            User.objects.create(
                username="metalgeek",
                email="metalgeek@octofit.edu",
                password=make_password("password123"),
                created_at=datetime.now(timezone.utc)
            ),
            User.objects.create(
                username="zerocool",
                email="zerocool@octofit.edu",
                password=make_password("password123"),
                created_at=datetime.now(timezone.utc)
            ),
            User.objects.create(
                username="crashoverride",
                email="crashoverride@octofit.edu",
                password=make_password("password123"),
                created_at=datetime.now(timezone.utc)
            ),
            User.objects.create(
                username="sleeptoken",
                email="sleeptoken@octofit.edu",
                password=make_password("password123"),
                created_at=datetime.now(timezone.utc)
            )
        ]

        # Create teams with scores
        teams = [
            Team.objects.create(
                name="Team Phoenix",
                score=150,
                description="A competitive team focused on high-intensity workouts."
            ),
            Team.objects.create(
                name="Team Atlas",
                score=200,
                description="A balanced team excelling in strength and endurance."
            ),
            Team.objects.create(
                name="Team Neptune",
                score=175,
                description="A team specializing in swimming and water sports."
            )
        ]
        
        # Add members to teams with balanced distribution
        teams[0].members.add(users[0], users[1])  # Team Phoenix
        teams[1].members.add(users[2], users[3])  # Team Atlas
        teams[2].members.add(users[4])            # Team Neptune

        # Create multiple activities per user over different dates
        activities = []
        for user in users:
            user_activities = [
                Activity.objects.create(
                    user=user,
                    activity_type="Running",
                    duration=timedelta(minutes=30 + hash(user.username) % 30),
                    created_at=datetime.now(timezone.utc) - timedelta(days=i)
                ) for i in range(3)  # 3 running activities over last 3 days
            ]
            activities.extend(user_activities)

            # Add some variety with different activity types
            varied_activities = [
                Activity.objects.create(
                    user=user,
                    activity_type=activity_type,
                    duration=timedelta(minutes=45 + hash(user.username + activity_type) % 45),
                    created_at=datetime.now(timezone.utc) - timedelta(days=i*2)
                ) for i, activity_type in enumerate(["Swimming", "Cycling", "Strength Training"])
            ]
            activities.extend(varied_activities)

        # Create leaderboard entries with meaningful scores based on activities
        for user in users:
            user_activities = Activity.objects.filter(user=user)
            activity_score = sum(act.duration.total_seconds() for act in user_activities)
            base_score = 100 + int(activity_score / 60)  # 1 point per minute of activity
            
            Leaderboard.objects.create(
                user=user,
                score=min(1000, base_score)  # Cap at 1000 points
            )

        # Create workouts with assignments to users
        workouts = [
            Workout.objects.create(
                name="Morning HIIT",
                description="High-intensity interval training with bodyweight exercises: 10 rounds of 30 seconds work, 30 seconds rest"
            ),
            Workout.objects.create(
                name="Endurance Run",
                description="5km continuous run at moderate pace with proper warm-up and cool-down stretches"
            ),
            Workout.objects.create(
                name="Power Cycling",
                description="Indoor cycling with varying resistance levels: 5 minutes easy, 5 minutes hard, repeat 4 times"
            ),
            Workout.objects.create(
                name="Swim Session",
                description="Mixed stroke swimming workout: 200m warm-up, 10x50m sprints, 200m cool-down"
            ),
            Workout.objects.create(
                name="Strength Training",
                description="Full body workout with free weights: 3 sets of 12 reps for major muscle groups"
            )
        ]

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(users)} users'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(teams)} teams'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(activities)} activities'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {Leaderboard.objects.count()} leaderboard entries'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(workouts)} workouts'))
