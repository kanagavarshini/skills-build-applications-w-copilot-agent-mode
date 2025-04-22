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
            {"username": "alice_wonder", "email": "alice@example.com", "team": "Team A"}
        ]
        db.users.insert_many(users)

        teams = [
            {"name": "Team A", "score": 150},
            {"name": "Team B", "score": 200}
        ]
        db.teams.insert_many(teams)

        activities = [
            {"name": "Running", "calories_burned": 300},
            {"name": "Cycling", "calories_burned": 250}
        ]
        db.activities.insert_many(activities)

        leaderboard = [
            {"username": "jane_smith", "score": 200},
            {"username": "john_doe", "score": 150}
        ]
        db.leaderboard.insert_many(leaderboard)

        workouts = [
            {"username": "john_doe", "activity": "Running", "duration": 30},
            {"username": "jane_smith", "activity": "Cycling", "duration": 45}
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))

if __name__ == "__main__":
    command = Command()
    command.handle()
