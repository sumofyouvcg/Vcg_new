from django.contrib.auth.models import Group 

try: # based on fixtures  in the util
    SITE_ADMIN          = Group.objects.get(pk = 1)
    COMPANY             = Group.objects.get(pk = 2)
    CAREGIVER           = Group.objects.get(pk = 3)
    CLIENT              = Group.objects.get(pk = 4)
    ADMIN               = Group.objects.get(pk = 5)
except:
    pass