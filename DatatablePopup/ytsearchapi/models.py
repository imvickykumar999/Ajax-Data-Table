from django.db import models

class YouTubeAPISearch(models.Model):
    search_query = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    location_radius = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    min_subscribers = models.IntegerField()
    max_results = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Unique representation for YouTubeAPISearch
        return f"{self.search_query} ({self.country}, {self.state}) - {self.created_at.strftime('%Y-%m-%d')}"

class YouTubeAPI(models.Model):
    search = models.ForeignKey(YouTubeAPISearch, on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    link = models.URLField()
    language = models.CharField(max_length=100, default='Not Specified')
    subscribers = models.IntegerField()
    description = models.TextField()
    location = models.CharField(max_length=100, default='Not Specified')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Unique representation for YouTubeAPI
        return f"{self.name} ({self.channel_id}) - {self.subscribers} subscribers"
