from django.contrib.auth.models import User
from django.db import models


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# use the default User model and this Profile model to represent user info
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        app_label = "monopoly"
