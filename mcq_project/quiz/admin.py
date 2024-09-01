from django.contrib import admin
from .models import Question, Solution, Score

class SolutionInline(admin.StackedInline):
    model = Solution
    extra = 1  # Number of extra forms to display by default

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [SolutionInline]  # Display SolutionInline in the Question admin
    list_display = ('question_text', 'correct_option')  # Customize to match your fields
    search_fields = ('question_text',)  # Add search fields if necessary

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('question', 'option_a', 'option_b', 'option_c', 'option_d')  # Customize this according to your fields
    search_fields = ('question__question_text', 'option_a', 'option_b', 'option_c', 'option_d')  # Add search fields if necessary

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'score', 'date_taken')  # Customize to match your fields
    search_fields = ('identifier',)  # Add search fields if necessary
    list_filter = ('date_taken',)  # Add filters if necessary
