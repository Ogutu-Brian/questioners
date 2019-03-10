from django.contrib import admin
"""
Registering the models to the admin interface
"""
from meetups.models import Meetup, Tag, Image
admin.site.register(Meetup)
admin.site.register(Tag)
admin.site.register(Image)
