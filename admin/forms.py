#-*-coding:utf-8-*-
import re
from django import forms
from django.contrib.auth.models import User
from member.models import UserProfile
from challenge.models import TagName
from django.core.exceptions import ValidationError

class TagForm(forms.Form):
    tag = forms.CharField(label=u'Tag', max_length=32)

class ProblemForm(forms.Form):
    GENDER_CHOICE = (
        ('1', 'Open'),
        ('0', 'Close'),
    )

    prob_name = forms.CharField(label=u'Title')
    prob_content = forms.CharField(label=u'Content', widget=forms.Textarea)
    prob_point = forms.CharField(label=u'Point')
    prob_auth = forms.CharField(label=u'Key', required=False)
    prob_flag = forms.ChoiceField(label=u'Open/Close', choices=GENDER_CHOICE)
    prob_tag = forms.ModelChoiceField(queryset=TagName.objects.all(), label=u'Tag', required=False)
    prob_file = forms.FileField(label=u'File', required=False)

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
    is_superuser = forms.TypedChoiceField(label=u'IS_SUPERUSER', coerce=int, choices=BOOL_CHOICE)
    is_active = forms.TypedChoiceField(label=u'IS_ACTIVE', coerce=int, choices=BOOL_CHOICE)

class ServerOnOffForm(forms.Form):
    ONOFF_CHOICE = (
        (0, "LEVEL 0"),
        (1, "LEVEL 1"),
        (2, "LEVEL 2"),
        (3, "LEVEL 3"),
    )

    on_off_level = forms.TypedChoiceField(label=u'On/Off Level', coerce=int, choices=ONOFF_CHOICE)

class RankModeChangeForm(forms.Form):
    MODE_CHOICE = (
        (0, "TABLE"),
        (1, "GRAPH"),
    )
    mode = forms.TypedChoiceField(label=u'Rank Mode Choice', coerce=str, choices=MODE_CHOICE)
