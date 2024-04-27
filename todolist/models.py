from django.db import models
import uuid
# Create your models here.
class Assignment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=200)
    due_date=models.DateTimeField()
    completed=models.BooleanField(default=False)
    def __str__(self):
        return self.name




class Selfstudy(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
    due_date=models.DateTimeField()
    completed=models.BooleanField(default=False)