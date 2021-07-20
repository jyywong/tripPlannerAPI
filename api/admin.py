from django.contrib import admin
from .models import Trip, TripEvent, MemberInvite, EventIdea, Alternative
# Register your models here.

admin.site.register(Trip)
admin.site.register(TripEvent)
admin.site.register(MemberInvite)
admin.site.register(EventIdea)
admin.site.register(Alternative)
