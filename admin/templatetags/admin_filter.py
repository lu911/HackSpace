from django import template
from django.utils.safestring import mark_safe
from member.models import UserProfile
register = template.Library()

def getObject(value, arg):
    return value[arg.tag]
def highlight(text, search):
    if(search is not ''):
        text=mark_safe(text.replace(search, "<span class='highlight'>%s</span>" % search))
    return text
def getScore(user):
    try:
        score = UserProfile.objects.get(user_id=user)
        return score.score
    except:
        return 0
register.filter('getObject', getObject)
register.filter('highlight', highlight)
register.filter('getScore', getScore)
