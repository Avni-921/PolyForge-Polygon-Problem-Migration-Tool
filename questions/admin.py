from django.contrib import admin
from .models import CodeforcesQuestion


@admin.register(CodeforcesQuestion)
class CodeforcesQuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'tags', 'url')
    list_filter = ('difficulty',)
    search_fields = ('title', 'tags', 'statement')
