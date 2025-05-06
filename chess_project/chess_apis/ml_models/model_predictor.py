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

def predict_win_probability(username, game_features, model_dir='chess_apis/ml_models/saved_models'):
        model, feature_names = load_win_prediction_model(username, model_dir)
        if model is None:
             return None
        
        df = pd.DataFrame([game_features])
        df_processed = prepare_features_for_model(df)

        missing_cols = set(feature_names) - set(df_processed.columns)
        for col in missing_cols:
             df_processed[col] = 0

        extra_cols = set(df_processed.columns) - set(feature_names)
        if extra_cols:
            df_processed = df_processed.drop(columns=extra_cols)

        df_processed = df_processed[feature_names]

        if hasattr(model, 'predict_proba'):
            try:
                probability = model.predict_proba(df_processed)[0][1]
            except:
            # Fallback to binary prediction
                probability = float(model.predict(df_processed)[0])
        else:
            probability = float(model.predict(df_processed)[0])
        
        return probability


