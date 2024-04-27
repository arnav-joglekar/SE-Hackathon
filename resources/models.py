from django.db import models
from django.contrib.auth.models import User

class Domain(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Resource(models.Model):
    STUDY_GUIDES = 'Study Guides'
    LECTURE_NOTES = 'Lecture Notes'
    PRACTICE_EXAMS = 'Practice Exams'
    USEFUL_WEBSITES = 'Useful Websites'

    CATEGORY_CHOICES = [
        (STUDY_GUIDES, 'Study Guides'),
        (LECTURE_NOTES, 'Lecture Notes'),
        (PRACTICE_EXAMS, 'Practice Exams'),
        (USEFUL_WEBSITES, 'Useful Websites'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resources/')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title
