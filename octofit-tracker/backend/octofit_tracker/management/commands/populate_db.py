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

        # Create teams
        team_a = Team.objects.create(
            name="Team A",
            score=150,
            description="A competitive team focused on running."
        )
        team_b = Team.objects.create(
            name="Team B",
            score=200,
            description="A team excelling in cycling."
        )
        team_c = Team.objects.create(
            name="Team C",
            score=120,
            description="A team passionate about swimming."
        )
        
        # Add members to teams
        team_a.members.add(User.objects.get(username="thundergod"))
        team_a.members.add(User.objects.get(username="zerocool"))
        team_b.members.add(User.objects.get(username="metalgeek"))
        team_b.members.add(User.objects.get(username="sleeptoken"))
        team_c.members.add(User.objects.get(username="crashoverride"))

        # Create activities for each user
        activities = [
            Activity.objects.create(
                user=User.objects.get(username="thundergod"),
                activity_type="Running",
                duration=timedelta(minutes=45)
            ),
            Activity.objects.create(
                user=User.objects.get(username="metalgeek"),
                activity_type="Cycling",
                duration=timedelta(hours=1)
            ),
            Activity.objects.create(
                user=User.objects.get(username="zerocool"),
                activity_type="Swimming",
                duration=timedelta(minutes=30)
            ),
            Activity.objects.create(
                user=User.objects.get(username="crashoverride"),
                activity_type="Running",
                duration=timedelta(minutes=60)
            ),
            Activity.objects.create(
                user=User.objects.get(username="sleeptoken"),
                activity_type="Cycling",
                duration=timedelta(minutes=90)
            )
        ]

        # Create leaderboard entries
        for user in users:
            Leaderboard.objects.create(
                user=user,
                score=100 + hash(user.username) % 100  # Random-ish score between 100-199
            )

        # Create workouts
        workouts = [
            Workout.objects.create(
                name="Morning HIIT",
                description="High-intensity interval training with bodyweight exercises"
            ),
            Workout.objects.create(
                name="Endurance Run",
                description="5km continuous run at moderate pace"
            ),
            Workout.objects.create(
                name="Power Cycling",
                description="Indoor cycling with varying resistance levels"
            ),
            Workout.objects.create(
                name="Swim Session",
                description="Mixed stroke swimming workout"
            ),
            Workout.objects.create(
                name="Strength Training",
                description="Full body workout with free weights"
            )
        ]

        self.stdout.write(self.style.SUCCESS('Successfully created {} users'.format(len(users))))
        self.stdout.write(self.style.SUCCESS('Successfully created {} teams'.format(Team.objects.count())))
        self.stdout.write(self.style.SUCCESS('Successfully created {} activities'.format(len(activities))))
        self.stdout.write(self.style.SUCCESS('Successfully created {} leaderboard entries'.format(Leaderboard.objects.count())))
        self.stdout.write(self.style.SUCCESS('Successfully created {} workouts'.format(len(workouts))))
