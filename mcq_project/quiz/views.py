from django.http import JsonResponse
from django.shortcuts import render
from .models import Question, Score
from .forms import QuizForm

def quiz_view(request):
    questions = Question.objects.all()[:10]  # Fetch the first 10 questions
    form = QuizForm(questions=questions)
    
    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            identifier = form.cleaned_data.get('identifier')
            for question in questions:
                correct_option = question.correct_option
                user_answer = form.cleaned_data.get(f'question_{question.id}')
                if user_answer == correct_option:
                    score += 1

            # Save the score in the database with an optional identifier
            Score.objects.create(identifier=identifier, score=score)
            return render(request, 'quiz/result.html', {'score': score, 'total': questions.count()})
    
    return render(request, 'quiz/quiz.html', {'form': form})

def score_data_view(request):
    scores = Score.objects.all().values('id', 'identifier', 'score', 'date_taken')
    return JsonResponse(list(scores), safe=False)

def score_list_view(request):
    return render(request, 'quiz/score_list.html')
