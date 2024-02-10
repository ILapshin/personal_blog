import time
import hashlib
import random

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from subscriptions.models import Subscription
from blogs.models import BlogPost


NUM_USERS = 1_000_000
NUM_SUBS = 100
NUM_POSTS = 50

def _get_random_string(seed: str):
    return hashlib.md5(seed.encode('utf-8')).hexdigest()

def _create_users(num_users=NUM_USERS):
    bulk_size = 1000
    n = num_users // bulk_size
    for k in range(n):
        bulk = []
        for i in range(bulk_size):
            random_string = _get_random_string(str(i + k * bulk_size))
            bulk.append(
                User(
                    username=random_string,
                    password=random_string,
                )
            )
        User.objects.bulk_create(bulk)
        print(f'{i + k * bulk_size} users created.')

def _create_subscriptions(num_users=NUM_USERS, num_subs=NUM_SUBS):
    users = User.objects.all()
    bulk = 500
    for b in range(len(users) // bulk):
        subs = []
        for user in users[b: b + bulk]:
            for i in range(num_subs):
                subs.append(
                    Subscription(
                        owner=random.choice(users),
                        subscriber=user
                    )
                )
        Subscription.objects.bulk_create(subs)
        print(f'{(b + 1) * num_subs * bulk} subscriptions created.')

def _create_posts(num_users=NUM_USERS, num_posts=NUM_POSTS):    
    users = User.objects.all()
    bulk = 500
    for b in range(bulk):
        posts = []
        for i in range(num_posts):
            for user in users[b: b + bulk]:
                user_id = random.randint(1, num_users)
                posts.append(
                    BlogPost(
                        owner=user,
                        title=f'Title for post {i}-{user.username}',
                        content=f'Mock content {i} {user.username}',
                    )
                )
        BlogPost.objects.bulk_create(posts)
        print(f'{(b + 1) * num_posts * bulk} posts created.')


class Command(BaseCommand):
    help = 'Fills the database with random mock objects'

    def handle(self, *args, **options):
        start = time.time()
        print('Start filling database...')
        print('Creating users...')
        # _create_users()
        print(f'{NUM_USERS} mock users created.')
        print('Creating subscriptions...')
        # _create_subscriptions()
        print(f'{NUM_SUBS * NUM_USERS} subscriptions created.')
        print('Creating blog posts...')
        _create_posts()
        print(f'{NUM_POSTS*NUM_USERS} posts created.')
        end = time.time()
        print(f'Filling database completed. Elapsed tims: {end - start}')