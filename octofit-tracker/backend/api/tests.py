from django.test import TestCase
from django.utils import timezone
from .models import User, Team, Activity, Leaderboard, Workout


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team='Test Team'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.team, 'Test Team')
        self.assertIsNotNone(self.user.created_at)
    
    def test_user_str(self):
        self.assertEqual(str(self.user), 'Test User')


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            members=['user1@example.com', 'user2@example.com']
        )
    
    def test_team_creation(self):
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'A test team')
        self.assertEqual(len(self.team.members), 2)
        self.assertIsNotNone(self.team.created_at)
    
    def test_team_str(self):
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    def setUp(self):
        self.activity = Activity.objects.create(
            user_email='test@example.com',
            activity_type='Running',
            duration=30,
            calories_burned=300,
            date=timezone.now(),
            notes='Morning run'
        )
    
    def test_activity_creation(self):
        self.assertEqual(self.activity.user_email, 'test@example.com')
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories_burned, 300)
        self.assertEqual(self.activity.notes, 'Morning run')
    
    def test_activity_str(self):
        self.assertEqual(str(self.activity), 'test@example.com - Running')


class LeaderboardModelTest(TestCase):
    def setUp(self):
        self.entry = Leaderboard.objects.create(
            user_email='test@example.com',
            user_name='Test User',
            team='Test Team',
            total_calories=1500,
            total_activities=5,
            rank=1
        )
    
    def test_leaderboard_creation(self):
        self.assertEqual(self.entry.user_email, 'test@example.com')
        self.assertEqual(self.entry.user_name, 'Test User')
        self.assertEqual(self.entry.team, 'Test Team')
        self.assertEqual(self.entry.total_calories, 1500)
        self.assertEqual(self.entry.total_activities, 5)
        self.assertEqual(self.entry.rank, 1)
    
    def test_leaderboard_str(self):
        self.assertEqual(str(self.entry), '1. Test User')


class WorkoutModelTest(TestCase):
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Morning Run',
            description='A quick morning run',
            activity_type='Running',
            duration=30,
            difficulty='Medium',
            calories_estimate=300
        )
    
    def test_workout_creation(self):
        self.assertEqual(self.workout.name, 'Morning Run')
        self.assertEqual(self.workout.description, 'A quick morning run')
        self.assertEqual(self.workout.activity_type, 'Running')
        self.assertEqual(self.workout.duration, 30)
        self.assertEqual(self.workout.difficulty, 'Medium')
        self.assertEqual(self.workout.calories_estimate, 300)
    
    def test_workout_str(self):
        self.assertEqual(str(self.workout), 'Morning Run')
