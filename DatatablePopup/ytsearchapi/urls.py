from django.urls import path
from . import views

urlpatterns = [
    path('search_filter_results', views.yt_index, name='yt_index'),  # Home page for YouTube search
    path('results/', views.yt_result, name='yt_result'),  # YouTube search results
    path('download/', views.download_view, name='download_view'),  # YouTube video downloader form
    path('download/selected/', views.download_selected_view, name='download_selected_view'),  # Video download action

    path('search_queries/<int:search_query_id>/', views.youtube_search_queries_list, name='youtube_search_queries_list'),
    path('search_query_results/<int:search_query_id>/', views.youtube_search_query_results, name='youtube_search_query_results'),
    path('search_list/', views.youtube_search_list, name='youtube_search_list'),
    path('', views.youtube_search_filter_results, name='youtube_search_filter_results'),

]
