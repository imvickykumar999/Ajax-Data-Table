from django.contrib import admin
from .models import YouTubeAPISearch, YouTubeAPI

@admin.register(YouTubeAPISearch)
class YouTubeAPISearchAdmin(admin.ModelAdmin):
    list_display = ('search_query', 'location', 'location_radius', 'country', 'state', 'min_subscribers', 'max_results', 'created_at')
    search_fields = ('search_query', 'country', 'state')  # Enable searching by these fields
    list_filter = ('country', 'state', 'created_at')  # Enable filtering by these fields
    ordering = ('-created_at',)  # Order by newest first

@admin.register(YouTubeAPI)
class YouTubeAPIAdmin(admin.ModelAdmin):
    list_display = ('name', 'channel_id', 'subscribers', 'location', 'language', 'created_at', 'search')
    search_fields = ('name', 'channel_id', 'location', 'language')  # Enable searching by these fields
    list_filter = ('location', 'language', 'created_at')  # Enable filtering by these fields
    ordering = ('-created_at',)  # Order by newest first
