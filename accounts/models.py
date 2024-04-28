from django.db import models
from django.contrib.auth.models import User
import uuid


DEPARTMENT_CHOICES = ['CSE', 'EXTC', 'MCA', 'CE']
YEAR_CHOICES = ['1', '2', '3', '4']
DOMAIN_CHOICES = ['Cyber Security', 'Blockchain', 'Data Science', 'AppDev', 'AIML', 'WebDev']


class Domain(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    DEPARTMENT_YEAR_CHOICES = [
        (department + ' ' + year, department + ' ' + year)
        for department in DEPARTMENT_CHOICES
        for year in YEAR_CHOICES
        if not (department == 'MCA' and (year == '3' or year == '4'))
    ]
    DOMAIN_CHOICES = [
        ('Cyber Security', 'Cyber Security'),
        ('Blockchain', 'Blockchain'),
        ('Data Science', 'Data Science'),
        ('AppDev', 'AppDev'),
        ('AIML', 'AIML'),
        ('WebDev', 'WebDev'),
    ]
    courses = models.CharField(max_length=6, choices=DEPARTMENT_YEAR_CHOICES)
    preferred_study_methods = models.TextField(blank=True)
    goals = models.TextField(blank=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    domains = models.ManyToManyField(Domain, related_name='user_profiles')

    def __str__(self):
        return self.user.username
    