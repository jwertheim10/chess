import requests
import json
import datetime
from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
from .user_data_methods import generate_user_data, generate_graphs


# Create your views here.
def index(request):
    username = request.GET.get('username')
    
    if not username:
        return render(request, 'get_apis.html')

    headers = {
    'User-Agent': 'chess/1.0'
    }

    is_testing = True
    user_api_url = f'https://api.chess.com/pub/player/{username}'
    user_stats_url = f'https://api.chess.com/pub/player/{username}/stats'
    user_games_url = f'https://api.chess.com/pub/player/{username}/games'

    if is_testing == True:
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
        
        try:
            with open('../../test_data/user_games_data.json', 'r') as file:
                user_games_data = json.load(file)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        try:
            response = requests.get(user_api_url, headers=headers)
            user_profile_data = response.json()
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        try:
            response = requests.get(user_stats_url, headers=headers)
            user_stats_data = response.json()
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

        try:
            response = requests.get(user_games_url, headers=headers)
            user_games_data = response.json()
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    

    chess_stats = []
    chess_types = ['blitz', 'rapid', 'daily', 'bullet']
    
    generate_user_data.main(chess_types, user_stats_data, chess_stats)
    rating_chart_over_time = generate_graphs.create_rating_chart_over_time(user_games_data, username, chess_types)

    context = {
        'rating_chart_over_time': rating_chart_over_time,
        'user_profile_data': user_profile_data,
        'chess_stats': chess_stats,
        'raw_stats_data': user_stats_data
    }
    
    return render(request, 'chess_profile.html', context)