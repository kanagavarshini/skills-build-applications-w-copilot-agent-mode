from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone
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
                team="Team A",
                age=30,
                gender="male",
                created_at=datetime.now(timezone.utc)
            ),
            User.objects.create(
                username="metalgeek",
                email="metalgeek@octofit.edu",
                password=make_password("password123"),
                team="Team B",
                age=25,
                gender="female",
                created_at=datetime.now(timezone.utc)
            ),
            User.objects.create(
                username="zerocool",
                email="zerocool@octofit.edu",
                password=make_password("password123"),
                team="Team A",
                age=28,
                gender="female",
                created_at=datetime.now(timezone.utc)
            ),
            User.objects.create(
                username="crashoverride",
                email="crashoverride@octofit.edu",
                password=make_password("password123"),
                team="Team C",
                age=35,
                gender="male",
                created_at=datetime.now(timezone.utc)
            ),
            User.objects.create(
                username="sleeptoken",
                email="sleeptoken@octofit.edu",
                password=make_password("password123"),
                team="Team B",
                age=22,
                gender="male",
                created_at=datetime.now(timezone.utc)
            )
        ]

        # Create teams
        teams = [
            Team.objects.create(
                name="Team A",
                score=150,
                members=["thundergod", "zerocool"],
                description="A competitive team focused on running.",
                created_at=datetime.now(timezone.utc)
            ),
            Team.objects.create(
                name="Team B",
                score=200,
                members=["metalgeek", "sleeptoken"],
                description="A team excelling in cycling.",
                created_at=datetime.now(timezone.utc)
            ),
            Team.objects.create(
                name="Team C",
                score=120,
                members=["crashoverride"],
                description="A team passionate about swimming.",
                created_at=datetime.now(timezone.utc)
            )
        ]

        # Create activities
        activities = [
            Activity.objects.create(
                name="Running",
                calories_burned=300,
                type="cardio",
                average_duration=30,
                created_at=datetime.now(timezone.utc)
            ),
            Activity.objects.create(
                name="Cycling",
                calories_burned=250,
                type="cardio",
                average_duration=45,
                created_at=datetime.now(timezone.utc)
            ),
            Activity.objects.create(
                name="Swimming",
                calories_burned=400,
                type="cardio",
                average_duration=60,
                created_at=datetime.now(timezone.utc)
            ),
            Activity.objects.create(
                name="Yoga",
                calories_burned=100,
                type="flexibility",
                average_duration=50,
                created_at=datetime.now(timezone.utc)
            )
        ]

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard.objects.create(
                username="metalgeek",
                score=200,
                rank=1,
                last_updated=datetime.now(timezone.utc)
            ),
            Leaderboard.objects.create(
                username="thundergod",
                score=150,
                rank=2,
                last_updated=datetime.now(timezone.utc)
            ),
            Leaderboard.objects.create(
                username="crashoverride",
                score=120,
                rank=3,
                last_updated=datetime.now(timezone.utc)
            ),
            Leaderboard.objects.create(
                username="zerocool",
                score=110,
                rank=4,
                last_updated=datetime.now(timezone.utc)
            ),
            Leaderboard.objects.create(
                username="sleeptoken",
                score=90,
                rank=5,
                last_updated=datetime.now(timezone.utc)
            )
        ]

        # Create workouts
        workouts = [
            Workout.objects.create(
                username="thundergod",
                activity="Running",
                duration=30,
                calories_burned=300,
                timestamp=datetime.now(timezone.utc)
            ),
            Workout.objects.create(
                username="metalgeek",
                activity="Cycling",
                duration=45,
                calories_burned=250,
                timestamp=datetime.now(timezone.utc)
            ),
            Workout.objects.create(
                username="zerocool",
                activity="Yoga",
                duration=50,
                calories_burned=100,
                timestamp=datetime.now(timezone.utc)
            ),
            Workout.objects.create(
                username="crashoverride",
                activity="Swimming",
                duration=60,
                calories_burned=400,
                timestamp=datetime.now(timezone.utc)
            ),
            Workout.objects.create(
                username="sleeptoken",
                activity="Running",
                duration=25,
                calories_burned=250,
                timestamp=datetime.now(timezone.utc)
            )
        ]

        self.stdout.write(self.style.SUCCESS('Database populated with test data successfully!'))
