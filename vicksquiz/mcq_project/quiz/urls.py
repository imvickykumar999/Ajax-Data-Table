from django.urls import path
from .views import quiz_view, score_data_view, score_list_view, question_details_view, answer_details_view

urlpatterns = [
    path('quiz/', quiz_view, name='quiz'),
    path('scores/data/', score_data_view, name='score_data'),
    path('', score_list_view, name='score_list'),
    path('question/<int:question_id>/', question_details_view, name='question_details'),
    path('answers/<int:score_id>/', answer_details_view, name='answer_details'),
]
