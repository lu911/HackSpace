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

def getRank(user):
    try:
        rankers = UserProfile.objects.all().order_by('-last_solve_time', 'score')
        rank = [ r.user.id for r in rankers ]
        return rank.index(user.id)+1
    except:
       return 0

register.filter('getObject', getObject)
register.filter('highlight', highlight)
register.filter('getScore', getScore)
register.filter('getRank', getRank)
