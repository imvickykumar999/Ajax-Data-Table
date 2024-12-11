from django.urls import path
from .views import load_rows, index

urlpatterns = [
    path('api/load-rows/', load_rows, name='load_rows'),
    path('', index, name='index'),  # Route for the index page
]
