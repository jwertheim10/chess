import os
import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import numpy as np
from .data_processor import extract_features_from_games, prepare_features_for_model, split_features_target

def train_win_prediction_model(games_data, username, model_dir = 'chess_apis/ml_models/saved_models'):
    os.makedirs(model_dir, exist_ok=True)
    
    # Process data
    df = extract_features_from_games(games_data, username)
    df_processed = prepare_features_for_model(df)
    X, y = split_features_target(df_processed)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    models = {
        'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'gradient_boosting': GradientBoostingClassifier(random_state=42),
        'logistic_regression': LogisticRegression(random_state=42, max_iter=1000)
    }

    results = {}
    best_model = None
    best_score = 0

    # I decided to use accuracy as my metric to measure the models as the main weakness is it treats the positive (wins)
    # and negatives (losses) as equally valuable. This is true here.

    for name, model in model:
        model.fit(X, y)
        y_predict = model.predict(X_test)
        score = accuracy_score(y_test, y_predict)
        results[name] = {
            'accuracy': score,
            'model': model
        }

        if score > best_score:
            best_model = model
            best_score = score

    model_path = os.path.join(model_dir, f'{username}_win_prediction_model.joblib')
    joblib.dump(best_model, model_path)
    feature_names = X.columns.tolist()
    feature_path = os.path.join(model_dir, f'{username}_feature_names.joblib')
    joblib.dump(feature_names, feature_path)

    return {
        'model_path': model_path,
        'feature_path': feature_path,
        'model_results': results,
    }