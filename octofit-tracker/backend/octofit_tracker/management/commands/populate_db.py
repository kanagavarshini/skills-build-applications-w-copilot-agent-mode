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

        # Create users with specific created_at times
        base_date = datetime(2025, 4, 1, tzinfo=timezone.utc)  # Start from April 1, 2025
        users = [
            User.objects.create(
                username="thundergod",
                email="thundergod@octofit.edu",
                password=make_password("password123"),
                created_at=base_date - timedelta(days=30)
            ),
            User.objects.create(
                username="metalgeek",
                email="metalgeek@octofit.edu",
                password=make_password("password123"),
                created_at=base_date - timedelta(days=28)
            ),
            User.objects.create(
                username="zerocool",
                email="zerocool@octofit.edu",
                password=make_password("password123"),
                created_at=base_date - timedelta(days=25)
            ),
            User.objects.create(
                username="crashoverride",
                email="crashoverride@octofit.edu",
                password=make_password("password123"),
                created_at=base_date - timedelta(days=20)
            ),
            User.objects.create(
                username="sleeptoken",
                email="sleeptoken@octofit.edu",
                password=make_password("password123"),
                created_at=base_date - timedelta(days=15)
            )
        ]

        # Create teams with specific focus areas
        teams = [
            Team.objects.create(
                name="Team Phoenix",
                score=150,
                description="A competitive team focused on high-intensity workouts and endurance training."
            ),
            Team.objects.create(
                name="Team Atlas",
                score=200,
                description="A balanced team excelling in strength training and CrossFit-style workouts."
            ),
            Team.objects.create(
                name="Team Neptune",
                score=175,
                description="A team specializing in swimming, water sports, and cardio activities."
            )
        ]
        
        # Add members to teams with balanced distribution
        teams[0].members.add(users[0], users[1])  # Team Phoenix
        teams[1].members.add(users[2], users[3])  # Team Atlas
        teams[2].members.add(users[4])            # Team Neptune

        # Create multiple activities per user over different dates with detailed descriptions
        activities = []
        activity_types = {
            "Running": ["5K training run", "Hill sprints session", "Recovery jog", "Speed intervals"],
            "Swimming": ["Freestyle practice", "Mixed stroke workout", "Endurance swim", "Sprint intervals"],
            "Cycling": ["Road bike training", "Indoor cycling class", "Mountain bike trail", "Recovery ride"],
            "Strength Training": ["Upper body focus", "Lower body day", "Full body workout", "Core training"],
            "HIIT": ["Tabata intervals", "Circuit training", "CrossFit WOD", "Bodyweight HIIT"]
        }

        for user in users:
            # Create activities for the last 7 days
            for days_ago in range(7):
                # Morning and evening workouts
                for session in ["Morning", "Evening"]:
                    activity_type = list(activity_types.keys())[hash(f"{user.username}{days_ago}{session}") % len(activity_types)]
                    description = activity_types[activity_type][hash(f"{user.username}{days_ago}") % len(activity_types[activity_type])]
                    
                    activity = Activity.objects.create(
                        user=user,
                        activity_type=activity_type,
                        duration=timedelta(minutes=30 + hash(f"{user.username}{days_ago}{session}") % 60),
                        created_at=datetime.now(timezone.utc) - timedelta(days=days_ago, 
                            hours=12 if session == "Evening" else 7)
                    )
                    activities.append(activity)

        # Create leaderboard entries with meaningful scores based on activities
        for user in users:
            user_activities = Activity.objects.filter(user=user)
            activity_score = sum(act.duration.total_seconds() for act in user_activities)
            base_score = 100 + int(activity_score / 60)  # 1 point per minute of activity
            
            Leaderboard.objects.create(
                user=user,
                score=min(1000, base_score)  # Cap at 1000 points
            )

        # Create team-specific workouts
        team_workouts = {
            "Team Phoenix": [
                ("Morning HIIT Challenge", "High-intensity interval training: 10 rounds of 30s work/30s rest. Exercises: Burpees, Mountain Climbers, Jump Squats, Push-ups."),
                ("Endurance Builder", "Progressive running workout: 5km run with alternating pace (1km easy, 1km moderate, 1km hard)."),
                ("Power Hour", "Circuit training with minimal rest: 45s work/15s transition, 4 rounds of 5 exercises.")
            ],
            "Team Atlas": [
                ("Strength Foundation", "5x5 compound lifts: Squats, Deadlifts, Bench Press, Rows. Progressive loading pattern."),
                ("CrossFit Classic", "For Time: 100 Pull-ups, 100 Push-ups, 100 Sit-ups, 100 Squats."),
                ("Olympic Lifting", "Technical session: Clean & Jerk and Snatch practice with form focus.")
            ],
            "Team Neptune": [
                ("Aqua Power", "Swimming endurance: 400m warm-up, 10x100m intervals, 200m cool-down."),
                ("Water Circuit", "Pool-based circuit: Treading water, Sprint laps, Underwater distance, Recovery strokes."),
                ("Technique Mastery", "Stroke refinement: Focus on freestyle and breaststroke technique.")
            ]
        }

        workouts = []
        for team in teams:
            for workout_name, workout_desc in team_workouts[team.name]:
                workout = Workout.objects.create(
                    name=f"{team.name}: {workout_name}",
                    description=workout_desc,
                    created_at=datetime.now(timezone.utc)
                )
                workouts.append(workout)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(users)} users'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(teams)} teams'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(activities)} activities'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {Leaderboard.objects.count()} leaderboard entries'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(workouts)} workouts'))
