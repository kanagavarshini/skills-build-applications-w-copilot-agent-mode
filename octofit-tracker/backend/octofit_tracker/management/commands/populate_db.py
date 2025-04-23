from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone, timedelta
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
import random

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create users with detailed profiles
        base_date = datetime(2025, 4, 1, tzinfo=timezone.utc)  # Start from April 1, 2025
        users = [
            User.objects.create(
                username="thundergod",
                email="thundergod@octofit.edu",
                password=make_password("password123"),
                created_at=base_date - timedelta(days=30),
                fitness_level="Advanced",
                fitness_goal="Athletic Performance",
                preferred_workout_time="Early Morning",
                height=185,  # in cm
                weight=80,   # in kg
                target_weight=75
            ),
            User.objects.create(
                username="metalgeek",
                email="metalgeek@octofit.edu",
                password=make_password("password123"),
                created_at=base_date - timedelta(days=28),
                fitness_level="Intermediate",
                fitness_goal="Muscle Gain",
                preferred_workout_time="Evening",
                height=175,
                weight=70,
                target_weight=75
            ),
            User.objects.create(
                username="zerocool",
                email="zerocool@octofit.edu",
                password=make_password("password123"),
                created_at=base_date - timedelta(days=25),
                fitness_level="Beginner",
                fitness_goal="Weight Loss",
                preferred_workout_time="Morning",
                height=170,
                weight=85,
                target_weight=70
            ),
            User.objects.create(
                username="crashoverride",
                email="crashoverride@octofit.edu",
                password=make_password("password123"),
                created_at=base_date - timedelta(days=20),
                fitness_level="Advanced",
                fitness_goal="Endurance",
                preferred_workout_time="Afternoon",
                height=178,
                weight=68,
                target_weight=68
            ),
            User.objects.create(
                username="sleeptoken",
                email="sleeptoken@octofit.edu",
                password=make_password("password123"),
                created_at=base_date - timedelta(days=15),
                fitness_level="Intermediate",
                fitness_goal="General Fitness",
                preferred_workout_time="Evening",
                height=168,
                weight=65,
                target_weight=65
            )
        ]

        # Create teams with specific focus areas and achievement tracking
        teams = [
            Team.objects.create(
                name="Team Phoenix",
                score=150,
                description="A competitive team focused on high-intensity workouts and endurance training.",
                specialty="HIIT",
                achievement_points=750,
                monthly_goal=1000,
                created_at=base_date - timedelta(days=25),
                last_challenge_date=base_date - timedelta(days=5)
            ),
            Team.objects.create(
                name="Team Atlas",
                score=200,
                description="A balanced team excelling in strength training and CrossFit-style workouts.",
                specialty="Strength Training",
                achievement_points=850,
                monthly_goal=1000,
                created_at=base_date - timedelta(days=25),
                last_challenge_date=base_date - timedelta(days=3)
            ),
            Team.objects.create(
                name="Team Neptune",
                score=175,
                description="A team specializing in swimming, water sports, and cardio activities.",
                specialty="Swimming",
                achievement_points=650,
                monthly_goal=1000,
                created_at=base_date - timedelta(days=25),
                last_challenge_date=base_date - timedelta(days=1)
            )
        ]
        
        # Add members to teams with roles and achievements
        team_roles = {
            teams[0]: {users[0]: "Captain", users[1]: "Member"},
            teams[1]: {users[2]: "Captain", users[3]: "Member"},
            teams[2]: {users[4]: "Captain"}
        }
        
        for team in teams:
            for user, role in team_roles[team].items():
                team.members.add(user)
                user.team_role = role
                user.team_join_date = base_date - timedelta(days=random.randint(15, 25))
                user.save()

        # Activity types with detailed metadata
        activity_types = {
            "Running": {
                "variations": ["5K training run", "Hill sprints session", "Recovery jog", "Speed intervals"],
                "intensity_levels": ["Low", "Medium", "High"],
                "calorie_burn_rate": 10,  # calories per minute
                "achievement_points": 10
            },
            "Swimming": {
                "variations": ["Freestyle practice", "Mixed stroke workout", "Endurance swim", "Sprint intervals"],
                "intensity_levels": ["Low", "Medium", "High"],
                "calorie_burn_rate": 8,
                "achievement_points": 12
            },
            "Cycling": {
                "variations": ["Road bike training", "Indoor cycling class", "Mountain bike trail", "Recovery ride"],
                "intensity_levels": ["Low", "Medium", "High"],
                "calorie_burn_rate": 7,
                "achievement_points": 8
            },
            "Strength Training": {
                "variations": ["Upper body focus", "Lower body day", "Full body workout", "Core training"],
                "intensity_levels": ["Low", "Medium", "High"],
                "calorie_burn_rate": 6,
                "achievement_points": 15
            },
            "HIIT": {
                "variations": ["Tabata intervals", "Circuit training", "CrossFit WOD", "Bodyweight HIIT"],
                "intensity_levels": ["Medium", "High"],
                "calorie_burn_rate": 12,
                "achievement_points": 20
            }
        }

        # Create activities with enhanced metadata
        activities = []
        for user in users:
            # Create activities for the last 14 days (2 weeks of history)
            for days_ago in range(14):
                # Morning and evening workouts with varying intensities
                for session in ["Morning", "Evening"]:
                    # Select activity type based on user's fitness goal and team specialty
                    if user.fitness_goal == "Weight Loss":
                        activity_weights = {"HIIT": 0.4, "Running": 0.3, "Swimming": 0.3}
                    elif user.fitness_goal == "Muscle Gain":
                        activity_weights = {"Strength Training": 0.6, "HIIT": 0.2, "Running": 0.2}
                    else:
                        activity_weights = {k: 1/len(activity_types) for k in activity_types.keys()}

                    activity_type = random.choices(
                        list(activity_weights.keys()),
                        weights=list(activity_weights.values())
                    )[0]
                    
                    variation = random.choice(activity_types[activity_type]["variations"])
                    intensity = random.choice(activity_types[activity_type]["intensity_levels"])
                    duration_minutes = 30 + hash(f"{user.username}{days_ago}{session}") % 60
                    calories_burned = duration_minutes * activity_types[activity_type]["calorie_burn_rate"]
                    achievement_points = activity_types[activity_type]["achievement_points"]
                    
                    if intensity == "High":
                        calories_burned *= 1.5
                        achievement_points *= 1.5
                    elif intensity == "Low":
                        calories_burned *= 0.7
                        achievement_points *= 0.7

                    activity = Activity.objects.create(
                        user=user,
                        activity_type=activity_type,
                        variation=variation,
                        intensity=intensity,
                        duration=timedelta(minutes=duration_minutes),
                        calories_burned=int(calories_burned),
                        achievement_points=int(achievement_points),
                        created_at=datetime.now(timezone.utc) - timedelta(
                            days=days_ago,
                            hours=12 if session == "Evening" else 7
                        ),
                        mood_rating=random.randint(1, 5),
                        perceived_effort=random.randint(1, 10)
                    )
                    activities.append(activity)

        # Create leaderboard entries with detailed statistics
        for user in users:
            user_activities = Activity.objects.filter(user=user)
            total_duration = sum((act.duration.total_seconds() for act in user_activities), 0)
            total_calories = sum((act.calories_burned for act in user_activities), 0)
            total_points = sum((act.achievement_points for act in user_activities), 0)
            
            Leaderboard.objects.create(
                user=user,
                score=min(1000, int(total_points)),  # Cap at 1000 points
                total_activities=len(user_activities),
                total_duration=timedelta(seconds=total_duration),
                total_calories=total_calories,
                streak_days=random.randint(5, 14),  # Current streak
                longest_streak=random.randint(15, 30),  # All-time best streak
                last_active=datetime.now(timezone.utc)
            )

        # Create detailed workouts with progression tracking
        team_workouts = {
            "Team Phoenix": [
                {
                    "name": "Morning HIIT Challenge",
                    "description": "High-intensity interval training: 10 rounds of 30s work/30s rest. Exercises: Burpees, Mountain Climbers, Jump Squats, Push-ups.",
                    "difficulty": "Advanced",
                    "equipment_needed": ["Timer", "Exercise Mat"],
                    "estimated_calories": 400,
                    "target_muscles": ["Full Body"],
                    "duration": timedelta(minutes=45)
                },
                {
                    "name": "Endurance Builder",
                    "description": "Progressive running workout: 5km run with alternating pace (1km easy, 1km moderate, 1km hard).",
                    "difficulty": "Intermediate",
                    "equipment_needed": ["Running Shoes"],
                    "estimated_calories": 500,
                    "target_muscles": ["Legs", "Core"],
                    "duration": timedelta(minutes=60)
                },
                {
                    "name": "Power Hour",
                    "description": "Circuit training with minimal rest: 45s work/15s transition, 4 rounds of 5 exercises.",
                    "difficulty": "Advanced",
                    "equipment_needed": ["Dumbbells", "Kettlebell", "Timer"],
                    "estimated_calories": 600,
                    "target_muscles": ["Full Body"],
                    "duration": timedelta(minutes=60)
                }
            ],
            "Team Atlas": [
                {
                    "name": "Strength Foundation",
                    "description": "5x5 compound lifts: Squats, Deadlifts, Bench Press, Rows. Progressive loading pattern.",
                    "difficulty": "Advanced",
                    "equipment_needed": ["Barbell", "Power Rack", "Weight Plates"],
                    "estimated_calories": 350,
                    "target_muscles": ["Full Body"],
                    "duration": timedelta(minutes=75)
                },
                {
                    "name": "CrossFit Classic",
                    "description": "For Time: 100 Pull-ups, 100 Push-ups, 100 Sit-ups, 100 Squats.",
                    "difficulty": "Intermediate",
                    "equipment_needed": ["Pull-up Bar"],
                    "estimated_calories": 450,
                    "target_muscles": ["Full Body"],
                    "duration": timedelta(minutes=45)
                },
                {
                    "name": "Olympic Lifting",
                    "description": "Technical session: Clean & Jerk and Snatch practice with form focus.",
                    "difficulty": "Advanced",
                    "equipment_needed": ["Olympic Barbell", "Bumper Plates"],
                    "estimated_calories": 300,
                    "target_muscles": ["Full Body"],
                    "duration": timedelta(minutes=90)
                }
            ],
            "Team Neptune": [
                {
                    "name": "Aqua Power",
                    "description": "Swimming endurance: 400m warm-up, 10x100m intervals, 200m cool-down.",
                    "difficulty": "Intermediate",
                    "equipment_needed": ["Swimming Pool", "Goggles"],
                    "estimated_calories": 450,
                    "target_muscles": ["Full Body"],
                    "duration": timedelta(minutes=60)
                },
                {
                    "name": "Water Circuit",
                    "description": "Pool-based circuit: Treading water, Sprint laps, Underwater distance, Recovery strokes.",
                    "difficulty": "Advanced",
                    "equipment_needed": ["Swimming Pool", "Pool Buoy"],
                    "estimated_calories": 400,
                    "target_muscles": ["Full Body"],
                    "duration": timedelta(minutes=45)
                },
                {
                    "name": "Technique Mastery",
                    "description": "Stroke refinement: Focus on freestyle and breaststroke technique.",
                    "difficulty": "Beginner",
                    "equipment_needed": ["Swimming Pool", "Kickboard", "Pull Buoy"],
                    "estimated_calories": 300,
                    "target_muscles": ["Full Body"],
                    "duration": timedelta(minutes=60)
                }
            ]
        }

        workouts = []
        for team in teams:
            team_captain = next(user for user, role in team_roles[team].items() if role == "Captain")
            for workout_data in team_workouts[team.name]:
                workout = Workout.objects.create(
                    name=f"{team.name}: {workout_data['name']}",
                    description=workout_data['description'],
                    difficulty=workout_data['difficulty'],
                    equipment_needed=", ".join(workout_data['equipment_needed']),
                    estimated_calories=workout_data['estimated_calories'],
                    target_muscles=", ".join(workout_data['target_muscles']),
                    duration=workout_data['duration'],
                    created_at=datetime.now(timezone.utc),
                    team=team,
                    created_by=team_captain,  # Using the actual User object
                    scheduled_time=base_date + timedelta(days=random.randint(1, 14)),
                    max_participants=20,
                    current_participants=random.randint(5, 15),
                    difficulty_rating=float(random.randint(35, 50))/10,  # 3.5-5.0 rating
                    success_rate=random.randint(70, 95)  # 70-95% success rate
                )
                workouts.append(workout)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(users)} users with detailed profiles'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(teams)} teams with achievements'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(activities)} activities with metadata'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {Leaderboard.objects.count()} detailed leaderboard entries'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(workouts)} comprehensive workouts'))
