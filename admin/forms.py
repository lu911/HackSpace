#-*-coding:utf-8-*-
import re
from django import forms
from django.contrib.auth.models import User
from member.models import UserProfile
from challenge.models import TagName
from django.core.exceptions import ValidationError

class TagForm(forms.Form):
    tag = forms.CharField(label=u'태그', max_length=32)
    
    
class ProblemForm(forms.Form):
    GENDER_CHOICE = (
        ('1', '공개'),
        ('0', '비공개'),
    )
    
    
    prob_name = forms.CharField(label=u'문제 이름')
    prob_content = forms.CharField(label=u'문제 내용', widget=forms.Textarea)
    prob_point = forms.CharField(label=u'문제 점수')
    prob_auth = forms.CharField(label=u'문제 정답')
    prob_flag = forms.ChoiceField(label=u'공개 여부', choices=GENDER_CHOICE)
    prob_tag = forms.ModelChoiceField(queryset=TagName.objects.all(), label=u'태그')
    
 