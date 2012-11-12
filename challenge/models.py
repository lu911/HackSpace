from django.db import models
from django.contrib.auth.models import User
from member.models import UserProfile

class Problem(models.Model):
    prob_name = models.CharField(max_length=128)
    prob_content = models.TextField()
    prob_point = models.IntegerField()
    prob_auth = models.CharField(max_length=256)
    prob_flag = models.IntegerField()

class AuthLog(models.Model):
    prob_id = models.ForeignKey(Problem)    
    user_id = models.ForeignKey(User)
    auth_type = models.IntegerField()
    auth_time = models.DateTimeField()
    auth_ip = models.CharField(max_length=16)
    auth_value = models.CharField(max_length=256)

class TagName(models.Model):
    tag = models.CharField(max_length=16)

class ProbTag(models.Model):
    prob_id = models.ForeignKey(Problem)
    tag_id = models.IntegerField()

    @classmethod
    def get_from_prob(cls,tag):
        return [prob_tag.prob_id for prob_tag in ProbTag.objects.filter(tag_id=tag)]
    
    @classmethod
    def get_from_all_prob(cls):
        return [prob_tag.prob_id for prob_tag in ProbTag.objects.all()]


