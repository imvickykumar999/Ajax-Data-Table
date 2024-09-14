import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from .models import YouTubeAPI, YouTubeAPISearch
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_date
from django.db.models import Q


def youtube_search_queries_list(request, search_query_id):
    search_query = get_object_or_404(YouTubeAPISearch, id=search_query_id)
    influencers = YouTubeAPI.objects.filter(search=search_query).order_by('-id')

    # Date filtering
    startdate = request.GET.get('startdate', '')
    enddate = request.GET.get('enddate', '')

    if startdate and enddate:
        startdate = parse_date(startdate)
        enddate = parse_date(enddate)
        if startdate and enddate:
            influencers = influencers.filter(created_at__date__range=(startdate, enddate))

    # Search functionality
    search_value = request.GET.get('search[value]', '')

    if search_value:
        influencers = influencers.filter(
            Q(name__icontains=search_value) |
            Q(channel_id__icontains=search_value) |
            Q(language__icontains=search_value) |
            Q(location__icontains=search_value) |
            Q(description__icontains=search_value) |
            Q(subscribers__icontains=search_value)
        )

    # Pagination
    paginator = Paginator(influencers, request.GET.get('length', 10))
    page_number = (int(request.GET.get('start', 0)) // paginator.per_page) + 1
    page_obj = paginator.get_page(page_number)

    # Data formatting for DataTables
    data = []
    for influencer in page_obj.object_list:
        data.append({
            'id': influencer.id,
            'name': influencer.name,
            'channel_id': influencer.channel_id,
            'link': influencer.link,
            'language': influencer.language,
            'subscribers': influencer.subscribers,
            'description': influencer.description,
            'location': influencer.location,
            'created_at': influencer.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    response = {
        'draw': int(request.GET.get('draw', 1)),
        'recordsTotal': influencers.count(),
        'recordsFiltered': paginator.count,
        'data': data,
    }

    return JsonResponse(response)


def youtube_search_query_results(request, search_query_id):
    search_topic = get_object_or_404(YouTubeAPISearch, id=search_query_id)
    return render(request, "Relationship-Manager/youtube_search_filter_results.html", 
                  {'search_query_id': search_query_id, "search_topic": search_topic})


def youtube_search_list(request):
    # Fetch all search queries ordered by the latest first
    searches = YouTubeAPISearch.objects.all().order_by('-id')

    # Date filtering
    startdate = request.GET.get('startdate', '')
    enddate = request.GET.get('enddate', '')

    if startdate and enddate:
        startdate = parse_date(startdate)
        enddate = parse_date(enddate)
        if startdate and enddate:
            searches = searches.filter(created_at__date__range=(startdate, enddate))

    # Search functionality
    search_value = request.GET.get('search[value]', '')

    if search_value:
        searches = searches.filter(
            Q(search_query__icontains=search_value) |
            Q(location__icontains=search_value) |
            Q(country__icontains=search_value) |
            Q(state__icontains=search_value)
        )

    # Pagination
    paginator = Paginator(searches, request.GET.get('length', 10))
    page_number = (int(request.GET.get('start', 0)) // paginator.per_page) + 1
    page_obj = paginator.get_page(page_number)

    # Data formatting for DataTables
    data = []
    for search in page_obj.object_list:
        data.append({
            'id': search.id,
            'search_query': search.search_query,
            'location': search.location,
            'location_radius': search.location_radius,
            'country': search.country,
            'state': search.state,
            'min_subscribers': search.min_subscribers,
            'max_results': search.max_results,
            'created_at': search.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    response = {
        'draw': int(request.GET.get('draw', 1)),
        'recordsTotal': searches.count(),
        'recordsFiltered': paginator.count,
        'data': data,
    }

    return JsonResponse(response)


def youtube_search_filter_results(request):
    return render(request, "Relationship-Manager/youtube_search_query_results.html")

################################# YouTube Video Downloader #####################################
# https://rapidapi.com/FarhanAliOfficial/api/youtube-downloader31/pricing

def list_formats(url):
    api_url = "https://youtube-downloader31.p.rapidapi.com/video.php"
    querystring = {"url": url}
    headers = {
        "x-rapidapi-key": "1dc9e6236dmshdfe058f825b062cp17212ejsnc424e02746a5",
        "x-rapidapi-host": "youtube-downloader31.p.rapidapi.com"
    }

    try:
        response = requests.get(api_url, headers=headers, params=querystring)
        data = response.json().get("data", {})

        video_with_audio = data.get("video_with_audio", [])
        thumbnail_url = data.get("video_info", {}).get("thumbnail", {}).get("thumbnails", [{}])[-1].get("url", '')

        # Filter out only MP4 formats with audio
        mp4_formats = [
            f for f in video_with_audio if "mp4" in f.get("mimeType", "")
        ]

        if not mp4_formats:
            return [], ''

        format_list = []
        for f in mp4_formats[::-1]:
            has_audio = f.get('has_audio', False)
            if has_audio:
                quality = f.get('quality', 'Unknown quality')
                fps = f.get('fps', 'Unknown FPS')
                format_str = f"{quality} - {fps} FPS"
                format_list.append({'url': f.get('url', ''), 'description': format_str})

        return format_list, thumbnail_url
    except Exception as e:
        print(f"Error listing formats: {e}")
        return [], ''

def stream_video(url):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk
    except requests.RequestException as e:
        print(f"Error streaming video: {e}")
        return

def download_view(request):
    if request.method == 'POST':
        url = request.POST['url']
        format_list, thumbnail_url = list_formats(url)
        return render(request, 'youtubedownloader/formats.html', {
            'formats': format_list, 
            'url': url, 
            'thumbnail_url': thumbnail_url, 
        })
    return render(request, 'youtubedownloader/index.html')

def download_selected_view(request):
    if request.method == 'POST':
        video_url = request.POST['url']
        selected_format_url = request.POST['format_url']
        
        if selected_format_url:
            response = StreamingHttpResponse(stream_video(selected_format_url), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="video.mp4"'
            return response
        else:
            return HttpResponse("Failed to download video.", status=500)
    return redirect('download_view')

################################# YouTube Channel Search API #####################################
# https://console.cloud.google.com/apis/credentials/key/83da1257-e24d-484f-924b-d7879612b6ff?project=imvickykumar999-1723015985916
API_KEY = 'AIzaSyAfeUNC-6MdtUfRX0BbrvB-gvGd7Wg7nsU'

def get_youtube_influencers(search_query, location, location_radius, country, state, min_subscribers, max_results):
    base_url = 'https://www.googleapis.com/youtube/v3/search'
    
    # Save the search query
    search_record = YouTubeAPISearch.objects.create(
        search_query=search_query,
        location=location,
        location_radius=location_radius,
        country=country,
        state=state,
        min_subscribers=min_subscribers,
        max_results=max_results
    )

    query = f'{search_query} '
    
    if country:
        query += f' {country}'
    if state:
        query += f' {state}'

    params = {
        'part': 'snippet',
        'q': query.strip(),
        'type': 'channel',
        'key': API_KEY,
        'maxResults': 50,
    }

    channels = []
    next_page_token = None

    while len(channels) < max_results:
        if next_page_token:
            params['pageToken'] = next_page_token

        response = requests.get(base_url, params=params)
        data = response.json()

        if 'error' in data:
            print(f"Error: {data['error']['message']}")
            break

        for item in data.get('items', []):
            channel_id = item['snippet']['channelId']
            channel_name = item['snippet']['channelTitle']
            youtube_link = f"https://www.youtube.com/channel/{channel_id}"

            # Fetch more details about the channel
            channel_url = 'https://www.googleapis.com/youtube/v3/channels'
            channel_params = {
                'part': 'snippet,statistics,brandingSettings',
                'id': channel_id,
                'key': API_KEY
            }
            channel_response = requests.get(channel_url, params=channel_params)
            channel_data = channel_response.json()

            if channel_data.get('items'):
                channel_info = channel_data['items'][0]
                channel_language = channel_info.get('brandingSettings', {}).get('channel', {}).get('defaultLanguage', 'Not Specified')
                subscriber_count = int(channel_info.get('statistics', {}).get('subscriberCount', 0))
                description = item['snippet']['description']
                country_or_state = channel_info.get('brandingSettings', {}).get('channel', {}).get('country', 'Not Specified')

                if subscriber_count >= min_subscribers:
                    # Save the channel only if it is within the max_results limit
                    influencer, created = YouTubeAPI.objects.get_or_create(
                        channel_id=channel_id,
                        defaults={
                            'search': search_record,  # Link to the search record
                            'name': channel_name,
                            'link': youtube_link,
                            'language': channel_language,
                            'subscribers': subscriber_count,
                            'description': description,
                            'location': country_or_state,
                        }
                    )

                    channels.append({
                        'name': channel_name,
                        'id': channel_id,
                        'link': youtube_link,
                        'language': channel_language,
                        'subscribers': subscriber_count,
                        'description': description,
                        'location': country_or_state 
                    })

                    if len(channels) >= max_results:
                        return channels

        next_page_token = data.get('nextPageToken')

        if not next_page_token:
            break

    return channels[:max_results]

def yt_index(request):
    return render(request, 'influencers/index.html')

def yt_result(request):
    search_query = request.GET.get('search_query', 'Blogging')
    location = request.GET.get('location', '28.7041,77.1025')
    location_radius = request.GET.get('location_radius', '500km')
    country = request.GET.get('country', 'India')
    state = request.GET.get('state', 'Delhi')
    min_subscribers = int(request.GET.get('min_subscribers', 10000))
    max_results = int(request.GET.get('max_results', 1000))

    channels = get_youtube_influencers(search_query, location, location_radius, country, state, min_subscribers, max_results)
    return render(request, 'influencers/result.html', {'channels': channels})
