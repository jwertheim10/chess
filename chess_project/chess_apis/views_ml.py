from django.shortcuts import render
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import base64
import io
import os
import numpy as np

from .ml_models.model_trainer import (
    train_win_prediction_model,
    # train_opening_recommendation_model,
    # train_optimal_play_time_model
)
from .ml_models.model_predictor import (
    predict_win_probability,
#     get_opening_recommendations,
#     get_optimal_play_times
)


def chess_ml_insights(request, username):

    model_dir = 'chess_apis/ml_models/saved_models'
    os.makedirs(model_dir, exist_ok=True)
    
    is_testing = True
    
    if is_testing:
        try:
            import json
            with open('../../test_data/user_games_data.json', 'r') as file:
                user_games_data = json.load(file)
        except Exception as e:
            return render(request, 'ml_error.html', {'error': str(e)})
    else:
        # In a real implementation, fetch from API
        import requests
        headers = {'User-Agent': 'chess/1.0'}
        user_games_url = f'https://api.chess.com/pub/player/{username}/games'
        
        try:
            response = requests.get(user_games_url, headers=headers)
            user_games_data = response.json()
        except Exception as e:
            return render(request, 'ml_error.html', {'error': str(e)})
    
    # Train models if they don't exist
    win_model_path = os.path.join(model_dir, f'{username}_win_prediction_model.joblib')
    if not os.path.exists(win_model_path):
        win_model_results = train_win_prediction_model(user_games_data, username, model_dir)
        # opening_recommendations = train_opening_recommendation_model(user_games_data, username, model_dir)
        # time_recommendations = train_optimal_play_time_model(user_games_data, username, model_dir)
    
    # # Get opening recommendations
    # opening_data = get_opening_recommendations(username, model_dir)
    # if opening_data is not None:
    #     opening_chart = create_opening_recommendation_chart(opening_data)
    # else:
    #     opening_chart = None
    
    # # Get time recommendations
    # time_data = get_optimal_play_times(username, model_dir)
    # if time_data is not None:
    #     time_chart = create_optimal_time_chart(time_data)
    # else:
    #     time_chart = None
    
    # Create a sample game for win prediction
    sample_game = {
        'user_color': 1,  # White
        'user_rating': 1200,
        'opponent_rating': 1200,
        'rating_diff': 0,
        'time_class': 'blitz',
        'opening': 'sicilian defense',
        'hour_of_day': 20,
        'day_of_week': 5
    }
    
    win_probability = predict_win_probability(username, sample_game, model_dir)
    
    context = {
        'username': username,
        # 'opening_chart': opening_chart,
        # 'time_chart': time_chart,
        'win_probability': win_probability * 100 if win_probability is not None else None,
    }
    
    return render(request, 'chess_ml_insights.html', context)