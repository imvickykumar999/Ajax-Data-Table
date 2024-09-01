from django.urls import path
from .views import quiz_view

urlpatterns = [
    path('quiz/', quiz_view, name='quiz'),
]
