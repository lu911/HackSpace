from django import template
from django.utils.safestring import mark_safe
register = template.Library()

def getObject(value, arg):
    return value[arg.tag]
def highlight(text, search):
    if(search is not ''):
        text=mark_safe(text.replace(search, "<span class='highlight'>%s</span>" % search))
    return text
register.filter('getObject', getObject)
register.filter('highlight', highlight)
