from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile


class Command(BaseCommand):
    help = 'Create missing profiles for existing users'

    def handle(self, *args, **options):
        users_without_profiles = []
        
        for user in User.objects.all():
            try:
                # Try to access the profile
                user.profile
            except Profile.DoesNotExist:
                users_without_profiles.append(user)
        
        if users_without_profiles:
            self.stdout.write(f'Found {len(users_without_profiles)} users without profiles.')
            
            for user in users_without_profiles:
                Profile.objects.create(user=user)
                self.stdout.write(f'Created profile for user: {user.username}')
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {len(users_without_profiles)} profiles.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('All users already have profiles.')
            )
