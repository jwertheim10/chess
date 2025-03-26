import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import base64
import io

def create_rating_chart_over_time(user_games_data, username, chess_types):
    data = user_games_data['games']
    rating_scores = {game_type: [] for game_type in chess_types}
    for game in data:
        if game['white']['username'] == username:
            rating_scores[game['time_class']].append(game['white']['rating'])
        else:
            rating_scores[game['time_class']].append(game['black']['rating'])


    print(rating_scores)
    df = pd.DataFrame([
        {'Chess Type': type_of_chess, 'Game Number': i+1, 'Rating': rating} 
        for type_of_chess, ratings in rating_scores.items() 
        for i, rating in enumerate(ratings)
    ])


    print(df)

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Game Number', y='Rating', hue='Chess Type')
    
    plot_file = io.BytesIO()
    plt.savefig(plot_file, format='png')
    plt.close()
    
    plot_file.seek(0)
    encoded_file = base64.b64encode(plot_file.read()).decode('utf-8')
    
    return encoded_file

    

