from meetups.models import Meetup, Tag, Image, Rsvp
from django.contrib import admin
"""
Registering the models to the admin interface
"""


class RsvpAdmin(admin.ModelAdmin):
    """
    Customizing the Rsvp panel
    """
    list_display = ["id", "responder", "meetup",
                    "response", "created_on", "updated_on"]
    list_filter = ("responder", "response")
    fieldsets = (
        ('Section 1', {
            'fields': ("responder", "response")
        }),
        ('Section 2', {
            'fields': ("meetup",)
        }),
    )


admin.site.register(Meetup)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Rsvp, RsvpAdmin)
