from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# use the default User model and this Profile model to represent user info
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    avatar = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return f"Profile [id:{self.id}, user_id:{self.user.id}, username:{self.user.username}]"

    class Meta:
        app_label = "monopoly"
