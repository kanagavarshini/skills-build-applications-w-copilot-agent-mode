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
        leaderboard_entries = [
            Leaderboard.objects.create(
                user=User.objects.get(username="metalgeek"),
                score=200
            ),
            Leaderboard.objects.create(
                user=User.objects.get(username="thundergod"),
                score=150
            ),
            Leaderboard.objects.create(
                user=User.objects.get(username="crashoverride"),
                score=120
            ),
            Leaderboard.objects.create(
                user=User.objects.get(username="zerocool"),
                score=110
            ),
            Leaderboard.objects.create(
                user=User.objects.get(username="sleeptoken"),
                score=90
            )
        ]

        # Create workouts
        workouts = [
            Workout.objects.create(
                name="High Intensity Running",
                description="Interval training with sprints and recovery periods"
            ),
            Workout.objects.create(
                name="Endurance Cycling",
                description="Long-distance cycling workout focusing on stamina"
            ),
            Workout.objects.create(
                name="Power Swimming",
                description="Mixed stroke swimming workout for full body fitness"
            ),
            Workout.objects.create(
                name="Strength Training",
                description="Full body workout with focus on major muscle groups"
            ),
            Workout.objects.create(
                name="HIIT Circuit",
                description="High-intensity interval training with mixed exercises"
            )
        ]

        self.stdout.write(self.style.SUCCESS('Database populated with test data successfully!'))
