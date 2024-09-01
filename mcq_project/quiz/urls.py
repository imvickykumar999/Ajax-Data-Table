from django.urls import path
from .views import quiz_view, score_data_view, score_list_view

urlpatterns = [
    path('quiz/', quiz_view, name='quiz'),
    path('scores/data/', score_data_view, name='score_data'),
    path('', score_list_view, name='score_list'),
]
