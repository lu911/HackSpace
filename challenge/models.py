from django.db import models

# Create your models here.

class Problem(models.Model):
    prob_name = models.CharField(max_length=128)
    prob_content = models.TextField()
    prob_point = models.IntegerField()
    prob_auth = models.CharField(max_length=256)

class AuthLog(models.Model):
    auth_type = models.IntegerField()
    auth_time = models.DateField()
    auth_ip = models.CharField(max_length=16)
    auth_value = models.CharField(max_length=256)
