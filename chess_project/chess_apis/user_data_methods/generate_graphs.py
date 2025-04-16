import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import base64
import io
from datetime import datetime, date



def create_rating_chart_over_time(user_games_data, username, chess_types):
    data = user_games_data['games']
    rating_scores = {game_type: [] for game_type in chess_types}
    for game in data:
        if game['white']['username'] == username:
            rating_scores[game['time_class']].append(game['white']['rating'])
        else:
            rating_scores[game['time_class']].append(game['black']['rating'])


    df = pd.DataFrame([
        {'Chess Type': type_of_chess, 'Game Number': i+1, 'Rating': rating} 
        for type_of_chess, ratings in rating_scores.items() 
        for i, rating in enumerate(ratings)
    ])

    plt.figure(figsize=(16, 8))
    sns.lineplot(data=df, x='Game Number', y='Rating', hue='Chess Type')
    
    plot_file = io.BytesIO()
    plt.savefig(plot_file, format='png')
    plt.close()
    
    plot_file.seek(0)
    encoded_file = base64.b64encode(plot_file.read()).decode('utf-8')
    
    return encoded_file


def create_openings_win_loss(user_games_data, username):
    data = user_games_data['games']
    openings_played = {}
    for game in data:
        url = game['eco']
        chess_opening = re.search(r'/([^/]+)$', url)
        chess_opening = chess_opening[1].replace('-', ' ')
        result = ''
        piece_color = 'white'
        if game['black']['username'] == username:
            piece_color = 'black'
        if game[piece_color]['result'] == '1/2-1/2':
            result = 'drawn'
        elif game[piece_color]['result'] == 'win':
            result = 'won'
        else:
            result = 'lost'
        if chess_opening not in openings_played:
            openings_played[chess_opening] = {
                'times_played': 0,
                'total_won': 0,
                'total_drawn': 0,
                'total_lost': 0,
                'times_played_white': 0,
                'times_played_black': 0,
                'times_won_white': 0,
                'times_won_black': 0,
                'times_lost_white': 0,
                'times_lost_black': 0,
                'times_drawn_white': 0,
                'times_drawn_black': 0,
                'last_played_at': None
            }
        openings_played[chess_opening]['times_played'] +=1
        openings_played[chess_opening]['last_played_at'] = datetime.fromtimestamp(game['end_time']).strftime('%B %d, %Y at %I:%M %p')
        openings_played[chess_opening][f'times_played_{piece_color}'] +=1
        openings_played[chess_opening][f'times_{result}_{piece_color}'] +=1
        openings_played[chess_opening][f'total_{result}'] +=1
    rows = []
    for opening_name, stats in openings_played.items():
        row = {
            'Opening': opening_name,
            'Times Played': stats['times_played'],
            'Total Won': stats['total_won'],
            'Total Drawn': stats['total_drawn'],
            'Total Lost': stats['total_lost'],
            'Times Played White': stats['times_played_white'],
            'Times Played Black': stats['times_played_black'],
            'Times Won White': stats['times_won_white'],
            'Times Won Black': stats['times_won_black'],
            'Times Lost White': stats['times_lost_white'],
            'Times Lost Black': stats['times_lost_black'],
            'Times Drawn White': stats['times_drawn_white'],
            'Times Drawn Black': stats['times_drawn_black'],
            'Last Played At': stats['last_played_at'],
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    min_games = 2
    df_filtered = df[df['Times Played'] >= min_games]

    plt.figure(figsize=(16, 8))
    bar_width = 0.25
    index = range(len(df_filtered))
    # White game outcomes
    plt.bar([i - bar_width for i in index], df_filtered['Times Won White'], bar_width, label='Times Won White', color='#ECFFDC')
    plt.bar([i - bar_width for i in index], df_filtered['Times Lost White'], bar_width, bottom=df_filtered['Times Won White'], label='Times Lost White', color='#F88379')
    plt.bar([i - bar_width for i in index], df_filtered['Times Drawn White'], bar_width, bottom=df_filtered['Times Won White']+df_filtered['Times Lost White'], label='Times Drawn White', color='#FFDEAD')
    # Black game outcomes
    plt.bar([i for i in index], df_filtered['Times Won Black'], bar_width, label='Times Won Black', color='#00A36C')
    plt.bar([i for i in index], df_filtered['Times Lost Black'], bar_width, bottom=df_filtered['Times Won Black'], label='Times Lost Black', color='#EC5800')
    plt.bar([i for i in index], df_filtered['Times Drawn Black'], bar_width, bottom=df_filtered['Times Won Black']+df_filtered['Times Lost Black'], label='Times Drawn Black', color='#F4C430')
    plt.title('Chess Openings: Wins, Losses, and Draws by Piece Color')
    plt.xlabel('Opening')
    plt.ylabel('Number of Games')
    plt.xticks([i - bar_width/2 for i in index], df_filtered['Opening'], rotation=45, ha='right')
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.legend(loc='upper right')
    plt.tight_layout()

    plot_file = io.BytesIO()
    plt.savefig(plot_file, format='png')
    plt.close()
    
    plot_file.seek(0)
    encoded_file = base64.b64encode(plot_file.read()).decode('utf-8')
    
    return encoded_file


def create_days_win_loss(user_games_data, username):
    data = user_games_data['games']
    days_played = {}
    for game in data:
        result = ''
        piece_color = 'white'
        if game['black']['username'] == username:
            piece_color = 'black'
        if game[piece_color]['result'] == '1/2-1/2':
            result = 'drawn'
        elif game[piece_color]['result'] == 'win':
            result = 'won'
        else:
            result = 'lost'
        date_time_of_game = datetime.fromtimestamp(game['end_time'])
        day_of_week = date_time_of_game.weekday()
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = day_names[day_of_week]
        if day not in days_played:
            days_played[day] = {
                'times_played': 0,
                'total_won': 0,
                'total_drawn': 0,
                'total_lost': 0,
                'times_played_white': 0,
                'times_played_black': 0,
                'times_won_white': 0,
                'times_won_black': 0,
                'times_lost_white': 0,
                'times_lost_black': 0,
                'times_drawn_white': 0,
                'times_drawn_black': 0,
                'last_played_at': None
            }
        days_played[day]['times_played'] +=1
        days_played[day]['last_played_at'] = datetime.fromtimestamp(game['end_time']).strftime('%B %d, %Y at %I:%M %p')
        days_played[day][f'times_played_{piece_color}'] +=1
        days_played[day][f'times_{result}_{piece_color}'] +=1
        days_played[day][f'total_{result}'] +=1

    rows = []
    for day, stats in days_played.items():
        row = {
            'Day': day,
            'Times Played': stats['times_played'],
            'Total Won': stats['total_won'],
            'Total Drawn': stats['total_drawn'],
            'Total Lost': stats['total_lost'],
            'Times Played White': stats['times_played_white'],
            'Times Played Black': stats['times_played_black'],
            'Times Won White': stats['times_won_white'],
            'Times Won Black': stats['times_won_black'],
            'Times Lost White': stats['times_lost_white'],
            'Times Lost Black': stats['times_lost_black'],
            'Times Drawn White': stats['times_drawn_white'],
            'Times Drawn Black': stats['times_drawn_black'],
            'Last Played At': stats['last_played_at'],
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    plt.figure(figsize=(10, 6))
    bar_width = 0.25
    index = range(len(df))
    plt.bar([i - bar_width for i in index], df['Total Won'], bar_width, label='Total Won', color='#00A36C')
    plt.bar([i - bar_width for i in index], df['Total Lost'], bar_width, bottom=df['Total Won'], label='Total Lost', color='#EC5800')
    plt.bar([i - bar_width for i in index], df['Total Drawn'], bar_width, bottom=df['Total Won']+df['Total Lost'], label='Total Drawn', color='#F4C430')
    plt.title('Chess Openings: Wins, Losses, and Draws by Day of Week')
    plt.xlabel('Day')
    plt.ylabel('Number of Games')
    plt.xticks([i - bar_width/2 for i in index], df['Day'], rotation=45, ha='right')
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.legend(loc='upper right')
    plt.tight_layout()

    plot_file = io.BytesIO()
    plt.savefig(plot_file, format='png')
    plt.close()
    
    plot_file.seek(0)
    encoded_file = base64.b64encode(plot_file.read()).decode('utf-8')
    return encoded_file