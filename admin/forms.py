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
    prob_file = forms.FileField(label=u'문제 파일', required=False)    
 
class CategoryForm(forms.Form):
    category_name = forms.CharField(label=u'Category')


class UserForm(forms.Form):
    BOOL_CHOICE = (
        (0, 'False'),
        (1, 'True'),
    )

    user_id = forms.IntegerField(widget=forms.HiddenInput())
    username = forms.CharField(label=u'ID', max_length=32)
    password = forms.CharField(label=u'Password', required=False,  widget=forms.PasswordInput(render_value=False))
    nickname = forms.CharField(label=u'Nickname', max_length=32)
    email = forms.EmailField(label=u'Email')
    is_staff = forms.TypedChoiceField(label=u'IS_STAFF', coerce=int, choices=BOOL_CHOICE)
    is_superuser = forms.TypedChoiceField(label=u'IS_SUPERUSER', coerce=int, choices=BOOL_CHOICE)
    is_active = forms.TypedChoiceField(label=u'IS_ACTIVE', coerce=int, choices=BOOL_CHOICE)
