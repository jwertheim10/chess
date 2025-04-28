import os
import joblib
import pandas as pd
import numpy as np
from .data_processor import prepare_features_for_model

def load_win_prediction_model(username, model_dir = 'chess_apis/ml_models/saved_models'):
    model_path = os.path.join(model_dir, f'{username}_win_prediction_model.joblib')
    feature_path = os.path.join(model_dir, f'{username}_feature_names.joblib')
    
    if not os.path.exists(model_path) or not os.path.exists(feature_path):
        return None, None
    
    model = joblib.load(model_path)
    feature_names = joblib.load(feature_path)
    
    return model, feature_names

