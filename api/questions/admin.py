from django.contrib import admin
from .models import Question,QuestionVote
# Register your models here.
admin.site.register(Question)
admin.site.register(QuestionVote)
