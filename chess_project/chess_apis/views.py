import requests
import json
import datetime
from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import base64
import io

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
    user_games_url = f'https://api.chess.com/pub/player/{username}/games'

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

    # try:
    #     response = requests.get(user_games_url, headers=headers)
    #     user_games_data = response.json()
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
    
    try:
        with open('../../test_data/user_games_data.json', 'r') as file:
            user_games_data = json.load(file)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    chess_stats = []
    chess_types = ['blitz', 'rapid', 'daily', 'bullet']
    
    for chess_type in chess_types:
        key = f'chess_{chess_type}'
        if key in user_stats_data:
            stat = {
                'type': chess_type.capitalize(),
                'current_rating': user_stats_data[key]['last']['rating'],
                'current_date': user_stats_data[key]['last']['date'],
                'best_rating': user_stats_data[key]['best']['rating'],
                'best_date': user_stats_data[key]['best']['date'],
                'wins': user_stats_data[key]['record']['win'],
                'losses': user_stats_data[key]['record']['loss'],
                'draws': user_stats_data[key]['record']['draw'],
                'total_games': user_stats_data[key]['record']['win'] + user_stats_data[key]['record']['loss'] + user_stats_data[key]['record']['draw'],
                'win_rate': round(user_stats_data[key]['record']['win'] / (user_stats_data[key]['record']['win'] + user_stats_data[key]['record']['loss'] + user_stats_data[key]['record']['draw']) * 100, 2),
                'loss_rate': round(user_stats_data[key]['record']['loss'] / (user_stats_data[key]['record']['win'] + user_stats_data[key]['record']['loss'] + user_stats_data[key]['record']['draw']) * 100, 2),
                'draw_rate': round(user_stats_data[key]['record']['draw'] / (user_stats_data[key]['record']['win'] + user_stats_data[key]['record']['loss'] + user_stats_data[key]['record']['draw']) * 100, 2)
            }
            chess_stats.append(stat)

    dat = create_rating_chart_over_time(user_games_data, username, chess_types)

    context = {
        'dat': dat,
        'user_profile_data': user_profile_data,
        'chess_stats': chess_stats,
        'raw_stats_data': user_stats_data
    }
    
    return render(request, 'chess_profile.html', context)


def create_rating_chart_over_time(user_games_data, username, chess_types):
    data = user_games_data['games']
    rating_scores = {game_type: [] for game_type in chess_types}
    for game_type in chess_types:
        for game in data:
            if game['time_class'] == game_type:
                if game['white']['username'] == username:
                    rating_scores[game_type].append(game['white']['rating'])
                else:
                    rating_scores[game_type].append(game['black']['rating'])


    print(rating_scores)
    df = pd.DataFrame([
        {'Chess Type': type_of_chess, 'Game Number': i, 'Rating': rating} 
        for type_of_chess, ratings in rating_scores.items() 
        for i, rating in enumerate(ratings)
    ])


    print(df)

    # Create the plot with explicit figure and axes
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Game Number', y='Rating', hue='Chess Type')
    
    # Save to a bytes buffer
    plot_file = io.BytesIO()
    plt.savefig(plot_file, format='png')
    plt.close()  # Close the plot to free up memory
    
    plot_file.seek(0)
    encoded_file = base64.b64encode(plot_file.read()).decode('utf-8')
    
    return encoded_file


    

