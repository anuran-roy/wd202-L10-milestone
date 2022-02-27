from django.db import models
from milestone.users.models import User

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta, timezone

STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("COMPLETED", "COMPLETED"),
    ("CANCELLED", "CANCELLED"),
)


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=100, default=STATUS_CHOICES[0][0]
    )
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    mail_time = models.TimeField(default=datetime.now().time())

    last_mailed = models.DateTimeField(
        null=True, blank=True, default=datetime.now(timezone.utc)
    )

    def __str__(self):
        return f"Profile: {self.user}" if self.user else "Profile: Anonymous"


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if not UserProfile.objects.filter(user=kwargs["instance"]).exists():
        new_profile = UserProfile(user=kwargs["instance"])
        new_profile.save()
