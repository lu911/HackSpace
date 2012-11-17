from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    score = models.IntegerField()
    last_solve_time = models.DateTimeField()
