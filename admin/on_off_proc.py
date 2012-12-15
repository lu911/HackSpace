from django.conf import settings

def CheckOnOff(request):
    onOffLevel = "0"
    try:
        onOffLevel = open("on_off", "r").read()
    except:
        onOffLevel = 0
    return {
        'on_off_level' : int(onOffLevel)
    }
