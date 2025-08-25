from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    attendance = models.IntegerField(default=0)
    grade = models.CharField(max_length=5, default="N/A")

    def __str__(self):
        return self.user.username
