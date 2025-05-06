import pandas as pd
import numpy as np
from datetime import datetime
import re

def extract_features_from_games(games_data, username):
    features = []

    for game in games_data['games']:
        user_color = 'White' if game['white']['username'] == username else 'Black'
        opponent_color = 'Black' if user_color == 'White' else 'White'

        result = 0
        if game[user_color]['result'] == 'win':
            result = 1
        elif game[user_color]['result'] == '1/2-1/2':
            result = 0.5
        
        opening_url = game['eco']
        opening_name = re.search(r'/([^/]+)$', opening_url)
        opening_name = opening_name[1].replace('-', ' ')

        game_time = game['end_time']
        hour_of_day = game_time.hour
        day_of_week = game_time.day

        user_rating = game[user_color]['rating']
        opponent_rating = game[opponent_color]['rating']
        rating_diff = user_rating - opponent_rating

        time_control = game['time_class']

        feature = {
            'user_color': 1 if user_color == 'white' else 0,
            'user_rating': user_rating,
            'opponent_rating': opponent_rating,
            'rating_diff': rating_diff,
            'time_control': time_control,
            'opening': opening_name,
            'hour_of_day': hour_of_day,
            'day_of_week': day_of_week,
            'result': result
        }

        features.append(feature)

    return pd.DataFrame(features)
    
def prepare_features_for_model(df):
    df_encoded = pd.get_dummies(df, columns=['time_class', 'opening'])
    df_encoded = df_encoded[df_encoded.result != 0.5]

    # We do this to ensure times (and dates) that are next to each other look next to each other in the model
    # If we don't do this, 11 PM (23:00) and midnight (00:00) look very far away
    # By doing this, we can have them appear close to each other (which they are)
    df_encoded['hour_sin'] = np.sin(2 * np.pi * df_encoded['hour_of_day'] / 24.0)
    df_encoded['hour_cos'] = np.cos(2 * np.pi * df_encoded['hour_of_day'] / 24.0)
    df_encoded['day_sin'] = np.sin(2 * np.pi * df_encoded['day_of_week'] / 7.0)
    df_encoded['day_cos'] = np.cos(2 * np.pi * df_encoded['day_of_week'] / 7.0)
    
    df_encoded.drop(['hour_of_day', 'day_of_week'], axis=1, inplace=True)
    
    return df_encoded

def split_features_target(df):
    X = df.drop('result', axis=1)
    y = df['result']
    
    return X, y