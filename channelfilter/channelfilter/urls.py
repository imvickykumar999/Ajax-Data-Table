from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ytsearchapi.urls')),  # Includes all URLs from the ytsearchapi app
]
