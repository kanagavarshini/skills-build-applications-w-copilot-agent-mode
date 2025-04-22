import pymongo
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate the MongoDB Atlas database with test data'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB Atlas
        client = pymongo.MongoClient('mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority')
        db = client['<dbname>']  # Replace <dbname> with your database name

        # Clear existing data
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Add test data
        users = [
            {"username": "john_doe", "email": "john@example.com", "team": "Team A"},
            {"username": "jane_smith", "email": "jane@example.com", "team": "Team B"},
        ]
        db.users.insert_many(users)

        teams = [
            {"name": "Team A", "members": ["john_doe"]},
            {"name": "Team B", "members": ["jane_smith"]},
        ]
        db.teams.insert_many(teams)

        activities = [
            {"user": "john_doe", "activity_type": "Running", "duration": 30, "calories_burned": 300},
            {"user": "jane_smith", "activity_type": "Cycling", "duration": 45, "calories_burned": 400},
        ]
        db.activities.insert_many(activities)

        leaderboard = [
            {"user": "john_doe", "points": 100},
            {"user": "jane_smith", "points": 120},
        ]
        db.leaderboard.insert_many(leaderboard)

        workouts = [
            {"name": "Morning Yoga", "description": "A relaxing yoga session", "duration": 60},
            {"name": "HIIT", "description": "High-intensity interval training", "duration": 30},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))

if __name__ == "__main__":
    command = Command()
    command.handle()
