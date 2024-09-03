
from .models import Question, Score, Solution, Answer
from django.http import JsonResponse
from django.shortcuts import render
from .forms import QuizForm

def quiz_view(request):
    questions = Question.objects.all()[:10]  # Fetch the first 10 questions
    form = QuizForm(questions=questions)
    
    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            identifier = form.cleaned_data.get('identifier')
            if not identifier:
            	identifier = 'unknown player'
            score_record = Score.objects.create(identifier=identifier, score=0)
            
            for question in questions:
                correct_option = question.correct_option
                user_answer = form.cleaned_data.get(f'question_{question.id}')
                
                # Save the user's answer
                Answer.objects.create(
                    score=score_record,
                    question=question,
                    selected_option=user_answer
                )
                
                if user_answer == correct_option:
                    score += 1

            # Update the score in the Score record
            score_record.score = score
            score_record.save()
            
            return render(request, 'quiz/result.html', {'score': score, 'total': questions.count()})
    
    return render(request, 'quiz/quiz.html', {'form': form})

def score_data_view(request):
    scores = Score.objects.all().values('id', 'identifier', 'score', 'date_taken')
    return JsonResponse(list(scores), safe=False)

def score_list_view(request):
    return render(request, 'quiz/score_list.html')

def question_details_view(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        solution = Solution.objects.get(question=question)
        response_data = {
            'id': question.id,
            'question_text': question.question_text,
            'option_a': solution.option_a,
            'option_b': solution.option_b,
            'option_c': solution.option_c,
            'option_d': solution.option_d,
            'correct_option': question.correct_option
        }
        return JsonResponse(response_data)
    except (Question.DoesNotExist, Solution.DoesNotExist):
        return JsonResponse({'error': 'Question or Solution not found.'}, status=404)

def answer_details_view(request, score_id):
    # Fetch all answers associated with the given score_id
    answers = Answer.objects.filter(score=score_id)
    
    # Prepare data for JSON response
    data = []
    for answer in answers:
        data.append({
            'id': answer.id,
            'question_text': answer.question.question_text,
            'selected_option': answer.selected_option,
            'option_a': answer.question.solution.option_a,
            'option_b': answer.question.solution.option_b,
            'option_c': answer.question.solution.option_c,
            'option_d': answer.question.solution.option_d,
            'correct_option': answer.question.correct_option
        })
    
    return JsonResponse(data, safe=False)
