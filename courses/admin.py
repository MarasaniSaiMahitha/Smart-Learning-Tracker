from django.contrib import admin
from .models import Topic, Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        'topic',
        'question_text'
    )

    list_filter = (
        'topic',
    )

    ordering = (
        'topic',
    )

admin.site.register(Topic)