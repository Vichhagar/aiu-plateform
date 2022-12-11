from django.contrib import admin
from .models import User, Activity, ActivityParticepationList

admin.site.register(User)
admin.site.register(Activity)
admin.site.register(ActivityParticepationList)
