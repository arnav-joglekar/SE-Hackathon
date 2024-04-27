from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    contributors = models.ManyToManyField(User, related_name='contributed_notes')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notes')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
