from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone, timedelta
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
import random
import json

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        base_date = datetime(2025, 4, 1, tzinfo=timezone.utc)

        # Predefined data
        badge_types = {
            "early_bird": "Complete 5 workouts before 7 AM",
            "night_owl": "Complete 5 workouts after 8 PM",
            "consistency": "Maintain a 7-day streak",
            "powerlifter": "Lift over 1000kg total in one session",
            "marathon": "Run over 42km in one week",
            "social": "Join 3 team workouts",
            "leader": "Lead a team workout",
            "all_rounder": "Try all workout types"
        }

        notification_prefs = {
            "workout_reminders": True,
            "team_updates": True,
            "achievement_alerts": True,
            "challenge_invites": True,
            "leaderboard_updates": False,
            "reminder_time": "1h_before",
            "email_notifications": True,
            "push_notifications": True
        }

        # User names and initial data
        user_data = [
            ("thundergod", "Athletic Performance", "Advanced", "Early Morning", 185, 80, 75),
            ("metalgeek", "Muscle Gain", "Intermediate", "Evening", 175, 70, 75),
            ("zerocool", "Weight Loss", "Beginner", "Morning", 170, 85, 70),
            ("crashoverride", "Endurance", "Advanced", "Afternoon", 178, 68, 68),
            ("sleeptoken", "General Fitness", "Intermediate", "Evening", 168, 65, 65)
        ]

        # Create users with enhanced features
        users = []
        for username, goal, level, pref_time, height, weight, target in user_data:
            weight_history = [
                {"date": (base_date - timedelta(days=x)).isoformat(),
                 "weight": weight - random.uniform(0, 0.5) * x}
                for x in range(30)
            ]

            personal_records = {
                "bench_press": random.randint(60, 120),
                "squat": random.randint(80, 160),
                "deadlift": random.randint(100, 200),
                "5k_time": str(timedelta(minutes=random.randint(20, 30))),
                "max_pushups": random.randint(30, 100)
            }

            user = User.objects.create(
                username=username,
                email=f"{username}@octofit.edu",
                password=make_password("password123"),
                created_at=base_date - timedelta(days=random.randint(15, 30)),
                fitness_level=level,
                fitness_goal=goal,
                preferred_workout_time=pref_time,
                height=height,
                weight=weight,
                target_weight=target,
                experience_points=random.randint(1000, 5000),
                level=random.randint(5, 20),
                badges=badge_types,
                weight_history=weight_history,
                notification_preferences=notification_prefs,
                personal_records=personal_records,
                streak_history=[{
                    "start": (base_date - timedelta(days=x*10)).isoformat(),
                    "length": random.randint(3, 14)
                } for x in range(5)]
            )
            users.append(user)

        # Team data with enhanced features
        team_data = [
            ("Team Phoenix", "HIIT", 750),
            ("Team Atlas", "Strength Training", 850),
            ("Team Neptune", "Swimming", 650)
        ]

        teams = []
        for name, specialty, points in team_data:
            team = Team.objects.create(
                name=name,
                score=random.randint(150, 200),
                description=f"A competitive team focused on {specialty}.",
                specialty=specialty,
                achievement_points=points,
                monthly_goal=1000,
                created_at=base_date - timedelta(days=25),
                last_challenge_date=base_date - timedelta(days=random.randint(1, 5)),
                announcements=[{
                    "date": (base_date - timedelta(days=x)).isoformat(),
                    "title": f"Team Update {x}",
                    "content": f"Important team announcement {x}"
                } for x in range(5)],
                challenge_history=[{
                    "date": (base_date - timedelta(days=x*7)).isoformat(),
                    "type": random.choice(["Distance", "Weight", "Duration"]),
                    "goal": random.randint(100, 1000),
                    "achieved": random.randint(50, 1200)
                } for x in range(4)],
                team_ranking=random.randint(1, 10),
                weekly_goals={
                    "total_workouts": 20,
                    "total_distance": 100,
                    "total_weight": 5000,
                    "member_participation": 0.8
                },
                events_calendar=[{
                    "date": (base_date + timedelta(days=x)).isoformat(),
                    "title": f"Team Event {x}",
                    "type": random.choice(["Competition", "Training", "Social"])
                } for x in range(1, 15)],
                team_stats={
                    "total_workouts_completed": random.randint(100, 500),
                    "avg_member_attendance": random.randint(70, 95),
                    "challenge_win_rate": random.randint(50, 90),
                    "member_satisfaction": random.randint(4, 5)
                }
            )
            teams.append(team)

        # Assign team members
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

        # Activity types with metadata
        activity_types = {
            "Running": {
                "variations": ["5K training run", "Hill sprints", "Recovery jog", "Speed intervals"],
                "intensity_levels": ["Low", "Medium", "High"],
                "calorie_burn_rate": 10,
                "achievement_points": 10
            },
            "Swimming": {
                "variations": ["Freestyle practice", "Mixed stroke workout", "Endurance swim", "Sprint intervals"],
                "intensity_levels": ["Low", "Medium", "High"],
                "calorie_burn_rate": 8,
                "achievement_points": 12
            },
            "Cycling": {
                "variations": ["Road bike training", "Indoor cycling", "Mountain bike trail", "Recovery ride"],
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

        # Create activities with enhanced tracking
        activities = []
        for user in users:
            for days_ago in range(14):
                for session in ["Morning", "Evening"]:
                    # Select activity type based on user's goals
                    if user.fitness_goal == "Weight Loss":
                        weights = {"HIIT": 0.4, "Running": 0.3, "Swimming": 0.3}
                        activity_type = random.choices(list(weights.keys()), 
                                                     weights=list(weights.values()))[0]
                    elif user.fitness_goal == "Muscle Gain":
                        weights = {"Strength Training": 0.6, "HIIT": 0.2, "Running": 0.2}
                        activity_type = random.choices(list(weights.keys()),
                                                     weights=list(weights.values()))[0]
                    else:
                        activity_type = random.choice(list(activity_types.keys()))

                    type_data = activity_types[activity_type]
                    
                    activity = Activity.objects.create(
                        user=user,
                        activity_type=activity_type,
                        variation=random.choice(type_data["variations"]),
                        intensity=random.choice(type_data["intensity_levels"]),
                        duration=timedelta(minutes=30 + hash(f"{user.username}{days_ago}{session}") % 60),
                        created_at=datetime.now(timezone.utc) - timedelta(
                            days=days_ago,
                            hours=12 if session == "Evening" else 7
                        ),
                        calories_burned=int(random.randint(200, 600)),
                        achievement_points=type_data["achievement_points"],
                        mood_rating=random.randint(1, 5),
                        perceived_effort=random.randint(1, 10),
                        location_data={
                            "start": {"lat": 40.7128, "lng": -74.0060},
                            "end": {"lat": 40.7580, "lng": -73.9855},
                            "route": [{"lat": 40.7128 + x*0.001, "lng": -74.0060 + x*0.001}
                                    for x in range(10)]
                        },
                        weather_conditions={
                            "temperature": random.randint(15, 25),
                            "conditions": random.choice(["Sunny", "Cloudy", "Rain"]),
                            "humidity": random.randint(40, 80),
                            "wind_speed": random.randint(0, 20)
                        },
                        heart_rate_data={
                            "avg": random.randint(120, 150),
                            "max": random.randint(160, 190),
                            "zones": {
                                "zone1": random.randint(5, 15),
                                "zone2": random.randint(20, 40),
                                "zone3": random.randint(30, 50),
                                "zone4": random.randint(10, 20),
                                "zone5": random.randint(0, 10)
                            }
                        },
                        notes=f"Felt {'great' if random.random() > 0.5 else 'tired'} during this {activity_type} session",
                        progress_photos=[f"photo_{x}.jpg" for x in range(random.randint(0, 3))]
                    )
                    activities.append(activity)

        # Create leaderboard entries with detailed stats
        for user in users:
            user_activities = Activity.objects.filter(user=user)
            total_duration = sum((act.duration.total_seconds() for act in user_activities), 0)
            total_calories = sum((act.calories_burned for act in user_activities), 0)
            total_points = sum((act.achievement_points for act in user_activities), 0)
            
            Leaderboard.objects.create(
                user=user,
                score=min(1000, int(total_points)),
                total_activities=len(user_activities),
                total_duration=timedelta(seconds=total_duration),
                total_calories=total_calories,
                streak_days=random.randint(5, 14),
                longest_streak=random.randint(15, 30),
                last_active=datetime.now(timezone.utc),
                monthly_rankings=[random.randint(1, 20) for _ in range(6)],
                achievement_breakdown={
                    "workout_points": random.randint(100, 500),
                    "challenge_points": random.randint(50, 200),
                    "streak_points": random.randint(50, 150),
                    "team_points": random.randint(100, 300)
                },
                badges_earned=list(badge_types.keys())[:random.randint(1, len(badge_types))],
                challenge_participations=[{
                    "challenge_id": x,
                    "result": random.choice(["winner", "completed", "participant"]),
                    "date": (base_date - timedelta(days=x*7)).isoformat()
                } for x in range(5)]
            )

        # Create workouts with comprehensive details
        workout_levels = {
            "Beginner": {"intensity": "60%", "rest": "90s", "modifications": "Assisted"},
            "Intermediate": {"intensity": "80%", "rest": "60s", "modifications": "Standard"},
            "Advanced": {"intensity": "100%", "rest": "30s", "modifications": "Weighted"}
        }

        team_workouts = {
            "Team Phoenix": [
                {
                    "name": "Morning Cardio Blast",
                    "description": "High-intensity interval training to kickstart your day.",
                    "difficulty": "Intermediate",
                    "equipment_needed": ["None"],
                    "estimated_calories": 400,
                    "target_muscles": ["Cardiovascular", "Legs", "Core"],
                    "duration": timedelta(minutes=30)
                },
                {
                    "name": "Evening Strength Circuit",
                    "description": "Full body strength workout to build muscle and endurance.",
                    "difficulty": "Advanced",
                    "equipment_needed": ["Dumbbells", "Kettlebell"],
                    "estimated_calories": 500,
                    "target_muscles": ["Full Body"],
                    "duration": timedelta(minutes=45)
                }
            ],
            "Team Atlas": [
                {
                    "name": "Powerlifting Session",
                    "description": "Focus on the big three lifts: squat, bench press, deadlift.",
                    "difficulty": "Advanced",
                    "equipment_needed": ["Barbell", "Weights"],
                    "estimated_calories": 600,
                    "target_muscles": ["Legs", "Chest", "Back"],
                    "duration": timedelta(minutes=60)
                },
                {
                    "name": "Mobility and Recovery",
                    "description": "Active recovery session focusing on mobility and flexibility.",
                    "difficulty": "Beginner",
                    "equipment_needed": ["None"],
                    "estimated_calories": 200,
                    "target_muscles": ["Full Body"],
                    "duration": timedelta(minutes=30)
                }
            ],
            "Team Neptune": [
                {
                    "name": "Endurance Swim",
                    "description": "Long distance swim to build endurance and technique.",
                    "difficulty": "Intermediate",
                    "equipment_needed": ["Swimsuit", "Goggles"],
                    "estimated_calories": 300,
                    "target_muscles": ["Shoulders", "Back", "Core"],
                    "duration": timedelta(minutes=45)
                },
                {
                    "name": "Sprint Intervals",
                    "description": "Short, high-intensity sprints to improve speed and power.",
                    "difficulty": "Advanced",
                    "equipment_needed": ["None"],
                    "estimated_calories": 350,
                    "target_muscles": ["Legs", "Core"],
                    "duration": timedelta(minutes=20)
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
                    created_by=team_captain,
                    scheduled_time=base_date + timedelta(days=random.randint(1, 14)),
                    max_participants=20,
                    current_participants=random.randint(5, 15),
                    difficulty_rating=float(random.randint(35, 50))/10,
                    success_rate=random.randint(70, 95),
                    prerequisites=["Basic mobility", "No injuries", f"Level {random.randint(1,5)} fitness"],
                    progression_levels=workout_levels,
                    media_links={
                        "tutorial": f"https://example.com/tutorials/workout_{team.name}_{workout_data['name']}",
                        "form_guide": f"https://example.com/guides/workout_{team.name}_{workout_data['name']}",
                        "preview": f"https://example.com/previews/workout_{team.name}_{workout_data['name']}"
                    },
                    coach_notes="Focus on proper form and scaling options for all levels",
                    substitute_exercises={
                        "push-ups": ["Wall push-ups", "Knee push-ups"],
                        "pull-ups": ["Band-assisted", "Negative pull-ups"],
                        "squats": ["Chair squats", "Box squats"]
                    }
                )
                workouts.append(workout)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(users)} users with detailed profiles'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(teams)} teams with achievements'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(activities)} activities with metadata'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {Leaderboard.objects.count()} detailed leaderboard entries'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(workouts)} comprehensive workouts'))
