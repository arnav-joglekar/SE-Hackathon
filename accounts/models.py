from django.db import models
from django.contrib.auth.models import User
import uuid


DEPARTMENT_CHOICES = ['CSE', 'EXTC', 'MCA', 'CE']
YEAR_CHOICES = ['1', '2', '3', '4']
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # academic_interests = models.TextField(blank=True)
    DEPARTMENT_YEAR_CHOICES = [
        (department + ' ' + year, department + ' ' + year)
        for department in DEPARTMENT_CHOICES
        for year in YEAR_CHOICES
        if not (department == 'MCA' and (year == '3' or year == '4'))
    ]
    courses = models.CharField(max_length=6, choices=DEPARTMENT_YEAR_CHOICES)
    preferred_study_methods = models.TextField(blank=True)
    goals = models.TextField(blank=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    def __str__(self):
        return self.user.username
    