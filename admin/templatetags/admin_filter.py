from django import template

register = template.Library()

def getObject(value, arg):
    return value[arg.tag]

register.filter('getObject', getObject)