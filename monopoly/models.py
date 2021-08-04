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

    @property
    def image_url(self):
        """
        Return self.photo.url if self.photo is not None,
        'url' exist and has a value, else, return None.
        """
        if self.avatar:
            return getattr(self.avatar, 'url', None)
        return None

    class Meta:
        app_label = "monopoly"
