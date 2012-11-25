from django.db import models
from django.contrib.auth.models import User
from member.models import UserProfile

from datetime import datetime
import md5

def get_filename(instance, filename):
    time = str(datetime.now());
    file = md5.md5(time + filename).hexdigest()
    return '%s.%s'%(file, filename.split('.')[-1])

class Problem(models.Model):
    prob_name = models.CharField(max_length=128)
    prob_content = models.TextField()
    prob_point = models.IntegerField()
    prob_auth = models.CharField(max_length=256)
    prob_flag = models.IntegerField()
    prob_solver = models.IntegerField(default=0)
    prob_file = models.FileField(upload_to=get_filename, null=True, blank=True)
    
    def get_prob_file(self):
        from django.conf import settings
        if self.prob_file:
            path = generate_filename(self.prob_file)
            return '%s%s'%(settings.MEDIA_URL, path)
        else:
            return ''
    
    def generate_filename(self,file):
        time = str(datetime.now());
        return md5.md5(time + file).hexdigest() 
        
class AuthLog(models.Model):
    prob_id = models.ForeignKey(Problem)
    user_id = models.ForeignKey(User)
    auth_type = models.IntegerField()
    auth_time = models.DateTimeField()
    auth_ip = models.CharField(max_length=16)
    auth_value = models.CharField(max_length=256)

class TagName(models.Model):
    tag = models.CharField(max_length=16)
    
    def __str__(self):
        return self.tag.encode('utf8')
    
    def getProblemCount(self):
        return len(ProbTag.get_from_prob(self))

class ProbTag(models.Model):
    prob_id = models.ForeignKey(Problem)
    tag_id = models.ForeignKey(TagName)

    @classmethod
    def get_from_prob(cls,tag):
        return [prob_tag.prob_id for prob_tag in ProbTag.objects.filter(tag_id=tag)]

    @classmethod
    def get_from_all_prob(cls):
        return [prob_tag.prob_id for prob_tag in ProbTag.objects.all()]


