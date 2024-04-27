from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # academic_interests = models.TextField(blank=True)
    courses = models.TextField(blank=True)
    preferred_study_methods = models.TextField(blank=True)
    goals = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    