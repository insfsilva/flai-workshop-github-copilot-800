from django.core.management.base import BaseCommand
from api.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        
        # Delete existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared'))
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Mightiest Heroes of Earth',
            members=[]
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League Champions',
            members=[]
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created {Team.objects.count()} teams'))
        
        # Create Users (Superheroes)
        self.stdout.write('Creating users...')
        
        marvel_heroes = [
            {'name': 'Tony Stark', 'email': 'ironman@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Steve Rogers', 'email': 'captainamerica@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Thor Odinson', 'email': 'thor@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Natasha Romanoff', 'email': 'blackwidow@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Bruce Banner', 'email': 'hulk@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Peter Parker', 'email': 'spiderman@marvel.com', 'team': 'Team Marvel'},
        ]
        
        dc_heroes = [
            {'name': 'Clark Kent', 'email': 'superman@dc.com', 'team': 'Team DC'},
            {'name': 'Bruce Wayne', 'email': 'batman@dc.com', 'team': 'Team DC'},
            {'name': 'Diana Prince', 'email': 'wonderwoman@dc.com', 'team': 'Team DC'},
            {'name': 'Barry Allen', 'email': 'flash@dc.com', 'team': 'Team DC'},
            {'name': 'Arthur Curry', 'email': 'aquaman@dc.com', 'team': 'Team DC'},
            {'name': 'Hal Jordan', 'email': 'greenlantern@dc.com', 'team': 'Team DC'},
        ]
        
        all_heroes = marvel_heroes + dc_heroes
        created_users = []
        
        for hero in all_heroes:
            user = User.objects.create(**hero)
            created_users.append(user)
        
        # Update team members
        team_marvel.members = [hero['email'] for hero in marvel_heroes]
        team_marvel.save()
        
        team_dc.members = [hero['email'] for hero in dc_heroes]
        team_dc.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {User.objects.count()} users'))
        
        # Create Activities
        self.stdout.write('Creating activities...')
        
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'HIIT']
        
        for user in created_users:
            # Create 5-10 activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                days_ago = random.randint(1, 30)
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 90)
                calories_burned = duration * random.randint(8, 15)
                
                Activity.objects.create(
                    user_email=user.email,
                    activity_type=activity_type,
                    duration=duration,
                    calories_burned=calories_burned,
                    date=datetime.now() - timedelta(days=days_ago),
                    notes=f'{activity_type} session for {user.name}'
                )
        
        self.stdout.write(self.style.SUCCESS(f'Created {Activity.objects.count()} activities'))
        
        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard...')
        
        leaderboard_data = []
        for user in created_users:
            user_activities = Activity.objects.filter(user_email=user.email)
            total_calories = sum(activity.calories_burned for activity in user_activities)
            total_activities = user_activities.count()
            
            leaderboard_data.append({
                'user_email': user.email,
                'user_name': user.name,
                'team': user.team,
                'total_calories': total_calories,
                'total_activities': total_activities
            })
        
        # Sort by total calories and assign ranks
        leaderboard_data.sort(key=lambda x: x['total_calories'], reverse=True)
        
        for rank, data in enumerate(leaderboard_data, start=1):
            Leaderboard.objects.create(
                rank=rank,
                **data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {Leaderboard.objects.count()} leaderboard entries'))
        
        # Create Workouts
        self.stdout.write('Creating workouts...')
        
        workouts = [
            {
                'name': 'Super Soldier Training',
                'description': 'High-intensity workout inspired by Captain America',
                'activity_type': 'HIIT',
                'duration': 45,
                'difficulty': 'Advanced',
                'calories_estimate': 600
            },
            {
                'name': 'Asgardian Strength',
                'description': 'Heavy weightlifting routine worthy of Thor',
                'activity_type': 'Weightlifting',
                'duration': 60,
                'difficulty': 'Advanced',
                'calories_estimate': 500
            },
            {
                'name': 'Speedster Sprint',
                'description': 'Fast-paced running intervals like The Flash',
                'activity_type': 'Running',
                'duration': 30,
                'difficulty': 'Intermediate',
                'calories_estimate': 400
            },
            {
                'name': 'Web-Slinger Circuit',
                'description': 'Agility and endurance workout like Spider-Man',
                'activity_type': 'HIIT',
                'duration': 40,
                'difficulty': 'Intermediate',
                'calories_estimate': 450
            },
            {
                'name': 'Amazonian Warrior',
                'description': 'Combat-ready workout inspired by Wonder Woman',
                'activity_type': 'Boxing',
                'duration': 50,
                'difficulty': 'Advanced',
                'calories_estimate': 550
            },
            {
                'name': 'Dark Knight Training',
                'description': 'Stealth and strength workout like Batman',
                'activity_type': 'Weightlifting',
                'duration': 55,
                'difficulty': 'Advanced',
                'calories_estimate': 520
            },
            {
                'name': 'Kryptonian Power',
                'description': 'Ultimate strength workout inspired by Superman',
                'activity_type': 'Weightlifting',
                'duration': 60,
                'difficulty': 'Expert',
                'calories_estimate': 650
            },
            {
                'name': 'Atlantean Swim',
                'description': 'Aquatic endurance training like Aquaman',
                'activity_type': 'Swimming',
                'duration': 45,
                'difficulty': 'Intermediate',
                'calories_estimate': 480
            },
            {
                'name': 'Zen Master Flow',
                'description': 'Peaceful yoga session for mind and body',
                'activity_type': 'Yoga',
                'duration': 60,
                'difficulty': 'Beginner',
                'calories_estimate': 250
            },
            {
                'name': 'Hero Cycling Challenge',
                'description': 'Long-distance cycling for endurance',
                'activity_type': 'Cycling',
                'duration': 75,
                'difficulty': 'Intermediate',
                'calories_estimate': 600
            },
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {Workout.objects.count()} workouts'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(f'Teams: {Team.objects.count()}')
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Activities: {Activity.objects.count()}')
        self.stdout.write(f'Leaderboard entries: {Leaderboard.objects.count()}')
        self.stdout.write(f'Workouts: {Workout.objects.count()}')
