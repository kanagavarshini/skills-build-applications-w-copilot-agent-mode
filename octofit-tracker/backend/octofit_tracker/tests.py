from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import timedelta
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import UserSerializer, TeamSerializer, ActivitySerializer, LeaderboardSerializer, WorkoutSerializer

class ModelTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create(
            username='testuser',
            email='test@octofit.edu',
            password='testpass123',
            fitness_level='Intermediate',
            fitness_goal='Weight Loss'
        )
        
        # Create test team
        self.team = Team.objects.create(
            name='Test Team',
            score=100,
            description='Test team description',
            specialty='HIIT'
        )
        self.team.members.add(self.user)

        # Create test activity
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='Running',
            duration=timedelta(minutes=30),
            intensity='High',
            calories_burned=300
        )

        # Create test leaderboard entry
        self.leaderboard = Leaderboard.objects.create(
            user=self.user,
            score=150,
            total_activities=1,
            streak_days=1
        )

        # Create test workout
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='Test workout description',
            difficulty='Intermediate',
            estimated_calories=400,
            duration=timedelta(minutes=45)
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.fitness_level, 'Intermediate')

    def test_team_creation(self):
        self.assertEqual(self.team.name, 'Test Team')
        self.assertTrue(self.user in self.team.members.all())

    def test_activity_creation(self):
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.calories_burned, 300)

    def test_leaderboard_creation(self):
        self.assertEqual(self.leaderboard.score, 150)
        self.assertEqual(self.leaderboard.user, self.user)

    def test_workout_creation(self):
        self.assertEqual(self.workout.name, 'Test Workout')
        self.assertEqual(self.workout.difficulty, 'Intermediate')

class APITests(APITestCase):
    def setUp(self):
        self.client = Client()
        # Create test data
        self.user = User.objects.create(
            username='apiuser',
            email='api@octofit.edu',
            password='apipass123'
        )
        self.team = Team.objects.create(
            name='API Team',
            score=100,
            description='API test team'
        )

    def test_api_root(self):
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)

    def test_user_list(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_team_list(self):
        response = self.client.get(reverse('team-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_activity(self):
        activity_data = {
            'user': self.user.id,
            'activity_type': 'Running',
            'duration': '00:30:00',
            'calories_burned': 300
        }
        response = self.client.post(reverse('activity-list'), activity_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_workout(self):
        workout_data = {
            'name': 'API Workout',
            'description': 'API test workout',
            'difficulty': 'Beginner',
            'estimated_calories': 200,
            'duration': '00:30:00'
        }
        response = self.client.post(reverse('workout-list'), workout_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class SerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='serializeruser',
            email='serializer@octofit.edu',
            password='serializerpass123'
        )
        self.team = Team.objects.create(
            name='Serializer Team',
            score=100,
            description='Serializer test team'
        )

    def test_user_serializer(self):
        serializer = UserSerializer(self.user)
        self.assertEqual(serializer.data['username'], 'serializeruser')
        self.assertEqual(serializer.data['email'], 'serializer@octofit.edu')

    def test_team_serializer(self):
        self.team.members.add(self.user)
        serializer = TeamSerializer(self.team)
        self.assertEqual(serializer.data['name'], 'Serializer Team')
        self.assertEqual(len(serializer.data['members']), 1)