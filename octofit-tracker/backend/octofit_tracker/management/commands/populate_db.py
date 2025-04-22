import pymongo
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate the MongoDB Atlas database with test data'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB Atlas
        client = pymongo.MongoClient('mongodb+srv://<kanagavarshini>:<MongoDB123@>@cluster0.mongodb.net/<your_dbname>?retryWrites=true&w=majority')
        db = client['//kanagavarshini:<MongoDB123@>']  # Replace '<your_dbname>' with your database name

        # Clear existing data
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Add test data
        users = [
            {"username": "john_doe", "email": "john@example.com", "team": "Team A", "age": 30, "gender": "male"},
            {"username": "jane_smith", "email": "jane@example.com", "team": "Team B", "age": 25, "gender": "female"},
            {"username": "alice_wonder", "email": "alice@example.com", "team": "Team A", "age": 28, "gender": "female"}
        ]
        db.users.insert_many(users)

        teams = [
            {"name": "Team A", "score": 150, "members": ["john_doe", "alice_wonder"], "description": "A competitive team focused on running."},
            {"name": "Team B", "score": 200, "members": ["jane_smith"], "description": "A team excelling in cycling."}
        ]
        db.teams.insert_many(teams)

        activities = [
            {"name": "Running", "calories_burned": 300, "type": "cardio", "average_duration": 30},
            {"name": "Cycling", "calories_burned": 250, "type": "cardio", "average_duration": 45}
        ]
        db.activities.insert_many(activities)

        leaderboard = [
            {"username": "jane_smith", "score": 200, "rank": 1},
            {"username": "john_doe", "score": 150, "rank": 2}
        ]
        db.leaderboard.insert_many(leaderboard)

        workouts = [
            {"username": "john_doe", "activity": "Running", "duration": 30, "timestamp": "2025-04-20T10:00:00Z"},
            {"username": "jane_smith", "activity": "Cycling", "duration": 45, "timestamp": "2025-04-21T15:00:00Z"}
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))

if __name__ == "__main__":
    command = Command()
    command.handle()
