import requests
import json
import datetime
from django.shortcuts import HttpResponse, render
from django.http import JsonResponse

# Create your views here.
def index(request):
    username = request.GET.get('username')
    
    if not username:
        return render(request, 'get_apis.html')

    headers = {
    'User-Agent': 'chess/1.0'
    }
    # Construct the API URL using the username
    user_api_url = f'https://api.chess.com/pub/player/{username}'
    user_stats_url = f'https://api.chess.com/pub/player/{username}/stats'

    # try:
    #     response = requests.get(user_api_url, headers=headers)
    #     user_profile_data = response.json()
    # except requests.exceptions.RequestException as e:
    #     return JsonResponse({'error': str(e)}, status=500)
    
    # try:
    #     response = requests.get(user_stats_url, headers=headers)
    #     user_stats_data = response.json()
    # except requests.exceptions.RequestException as e:
    #     return JsonResponse({'error': str(e)}, status=500)
    
    # the below is for testing when i cannot access the chess.com api
    try:
        with open('../../test_data/user_profile_data.json', 'r') as file:
            user_profile_data = json.load(file)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    try:
        with open('../../test_data/user_stats_data.json', 'r') as file:
            user_stats_data = json.load(file)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'chess_profile.html', 
                  {'user_profile_data': user_profile_data, 'user_stats_data': user_stats_data})