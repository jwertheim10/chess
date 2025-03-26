

def main(chess_types, user_stats_data, chess_stats):
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