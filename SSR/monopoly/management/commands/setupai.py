from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from monopoly.models import Profile


class Command(BaseCommand):
    help = 'Setup AI players'

    def handle(self, *args, **options):
        try:
            user = User.objects.create(username="AI", password="AI")
            Profile.objects.create(user=user)
        except User.DoesNotExist:
            raise CommandError('User does not exist')
        self.stdout.write(self.style.SUCCESS('Successfully setup ai players poll'))
