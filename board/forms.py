from django import forms
from models import Category
from django.db.models import Q

class PostForm(forms.Form):
    title = forms.CharField(label=u'title', widget=forms.TextInput())
    category = forms.ModelChoiceField(queryset=Category.objects.filter(~Q(id=1)))
    content = forms.CharField(label=u'content', widget=forms.Textarea())
