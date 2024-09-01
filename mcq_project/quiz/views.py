from django.shortcuts import render
from .models import Question
from .forms import QuizForm

def quiz_view(request):
    questions = Question.objects.all()[:10]  # Fetch the first 10 questions
    form = QuizForm(questions=questions)
    
    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                correct_option = question.correct_option
                user_answer = form.cleaned_data.get(f'question_{question.id}')
                if user_answer == correct_option:
                    score += 1
            return render(request, 'quiz/result.html', {'score': score, 'total': questions.count()})
    
    return render(request, 'quiz/quiz.html', {'form': form})
