import pandas as pd
import numpy as np
import os
import logging
import click 

from helpers import is_relevant_game, timing, setup_logger

setup_logger()

INPUT_PATH = './processed_data'
OUTPUT_PATH = './games_with_cp_metrics.csv'
MIN_ELO = 2000
NUM_OPENING_MOVES = 10
MIN_REMAINING_MOVES = 10


@click.command()
@click.option("--input_path", default=INPUT_PATH, type=str)
@click.option("--output_path", default=OUTPUT_PATH, type=str)
@click.option("--min_elo", default=MIN_ELO, type=int)
@click.option("--num_opening_moves", default=NUM_OPENING_MOVES, type=int)
@click.option("--min_remaining_moves", default=MIN_REMAINING_MOVES, type=int)
@timing
def create_centipawn_df(input_path, min_elo, num_opening_moves, min_remaining_moves, output_path) -> pd.DataFrame:
    """Reads all data (output of `process_pgns.py`) and combines into a single dataframe.
    
    Filters out players with sub `min_elo` rating.
    Removes `num_opening_moves` opening moves.
    Requires at least `min_remaining_moves` number of remaining moves.

    Dataframe saved to `output_path`.
    """

    centipawn_metrics = []
    for filename in os.listdir(input_path):
        data = pd.read_pickle(f'{input_path}/{filename}').to_dict('records')
        for game in data:
            if not is_relevant_game(game):
                continue
            
            event = game['event']
            site = game['site']
            round = game['round']
            date = game['date']
            
            white_player = game['white_player']
            white_elo = game['white_elo']
            black_player = game['black_player']
            black_elo = game['black_elo']
            white_cp_losses = game['white_cp_losses'][num_opening_moves:]
            black_cp_losses = game['black_cp_losses'][num_opening_moves:]
            
            if white_elo is not None and white_elo > min_elo and len(white_cp_losses) >= min_remaining_moves:
                # Filter out opening moves
                metrics = {}
                metrics['event'] = event
                metrics['site'] = site
                metrics['round'] = round
                metrics['date'] = date
                metrics['player'] = white_player
                metrics['elo'] = white_elo
                metrics['color'] = 'white'
                metrics['opponent'] = black_player
                metrics['result'] = 'won' if game['result'] == '1-0' else ('lost' if game['result'] == '0-1' else 'draw')
                cp_losses = white_cp_losses
                metrics['avg_cp_loss'] = np.mean(cp_losses)
                metrics['std_cp_loss'] = np.std(cp_losses)
                centipawn_metrics.append(metrics)

            if black_elo is not None and black_elo > min_elo and len(black_cp_losses) >= min_remaining_moves:
                metrics = {}
                metrics['event'] = event
                metrics['site'] = site
                metrics['round'] = round
                metrics['date'] = date
                metrics['player'] = black_player
                metrics['elo'] = black_elo
                metrics['color'] = 'black'
                metrics['opponent'] = white_player
                metrics['result'] = 'won' if game['result'] == '0-1' else ('lost' if game['result'] == '1-0' else 'draw')
                cp_losses = black_cp_losses
                metrics['avg_cp_loss'] = np.mean(cp_losses)
                metrics['std_cp_loss'] = np.std(cp_losses)
                centipawn_metrics.append(metrics)
                
    df = pd.DataFrame(centipawn_metrics)
    # Remove any duplicates
    dup_cols = df.columns.to_list()
    dup_cols.remove('avg_cp_loss')
    dup_cols.remove('std_cp_loss')
    pre_len = len(df)
    df = df.drop_duplicates(subset=dup_cols)
    post_len = len(df)
    logging.info(f'Num duplicates: {pre_len - post_len}')

    # Remove obvious outliers 
    df = df[df['avg_cp_loss'] <= 100]
    df.to_csv(output_path, index=False)
        

if __name__ == '__main__':
    create_centipawn_df()