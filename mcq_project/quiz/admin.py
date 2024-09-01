from django.contrib import admin
from .models import Question, Solution

class SolutionInline(admin.TabularInline):
    model = Solution

class QuestionAdmin(admin.ModelAdmin):
    inlines = [SolutionInline]

admin.site.register(Question, QuestionAdmin)
