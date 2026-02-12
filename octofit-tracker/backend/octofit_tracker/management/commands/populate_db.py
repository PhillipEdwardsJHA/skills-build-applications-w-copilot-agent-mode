
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear collections directly using pymongo for ObjectIdField compatibility
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db['leaderboard'].delete_many({})
        db['activities'].delete_many({})
        db['workouts'].delete_many({})
        db['users'].delete_many({})
        db['teams'].delete_many({})

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        # Create users
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        # Create activities
        Activity.objects.create(user=users[0], type='Running', duration=30, date=timezone.now().date())
        Activity.objects.create(user=users[1], type='Cycling', duration=45, date=timezone.now().date())
        Activity.objects.create(user=users[2], type='Swimming', duration=60, date=timezone.now().date())
        Activity.objects.create(user=users[3], type='Yoga', duration=20, date=timezone.now().date())

        # Create workouts
        w1 = Workout.objects.create(name='Pushups', description='Upper body strength')
        w2 = Workout.objects.create(name='Squats', description='Lower body strength')
        w1.suggested_for.set([users[0], users[2]])
        w2.suggested_for.set([users[1], users[3]])

        # Create leaderboard
        Leaderboard.objects.create(user=users[0], score=120)
        Leaderboard.objects.create(user=users[1], score=110)
        Leaderboard.objects.create(user=users[2], score=130)
        Leaderboard.objects.create(user=users[3], score=100)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
