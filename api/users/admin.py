from django.contrib import admin
"""
Register user models
"""
from .models import User

admin.site.register(User)
