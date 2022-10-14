import chess
import chess.engine
import chess.pgn
from typing import Callable, Union, List
from datetime import datetime
import time
import numpy as np
from functools import wraps
import logging

def setup_logger():
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("logs/debug.log"),
        logging.StreamHandler()
    ])

def evaluate_position(board: chess.Board , engine: chess.engine.SimpleEngine, limit: chess.engine.Limit):
   info = engine.analyse(board, limit)
   return info['score'].white().score(mate_score=1000)

def parse_elo_rating(rating_str: str) -> Union[int, None]:
    try: 
        rating = int(rating_str)
    except ValueError:
        return None
    return rating

def parse_date(date_str: str) -> Union[datetime, None]:
    try:
        date = datetime.strptime(date_str, '%Y.%m.%d')
    except:
        try:
            date = datetime.strptime(date_str, '%Y.??.??')
        except:
            return None

    return date 

def read_games(pgn_path: str) -> List[chess.pgn.Game]:
    games = []
    with open(pgn_path) as file:
        while True:
            game = chess.pgn.read_game(file)
            if game is None:
                break  # end of games in file
            games.append(game)
    return games

def is_relevant_game(game: dict):
    event = game['event']
    site = game['event']
    return 'blitz' not in event.lower() \
        and 'rapid' not in event.lower() \
        and 'speed' not in event.lower() \
        and ' sim' not in event.lower() \
        and 'bullet' not in event.lower() \
        and 'blindfold' not in event.lower() \
        and '.com' not in site.lower() \
        and '.org' not in site.lower() \
        and '.net' not in site.lower()
        

def timing(func: Callable):
    """Decorator to time any function."""
    @wraps(func)
    def wrap(*args, **kw):
        ts = time.time()
        result = func(*args, **kw)
        te = time.time()
        logging.info(f'{func.__name__} done in {(te-ts):.3f}s.')
        return result
    return wrap

def save_to_npy(path: str, data: List[dict], append=True):
    """Saves list of dicts to file as .npy file (pickled).
    
    If already exists, and append=True, it will append.
    Otherwise, replace the already existing, or create new.
    """

    write_data = []
    if append:
        try:
            existing_output = np.load(path, allow_pickle=True).tolist()
            for i, el in enumerate(existing_output):
                existing_output[i]['white_cp_losses'] = tuple(existing_output[i]['white_cp_losses'].tolist())
                existing_output[i]['black_cp_losses'] = tuple(existing_output[i]['black_cp_losses'].tolist())
        except FileNotFoundError:
            pass
        else:
            write_data.extend(existing_output)
    
    write_data.extend(data)

    # Remove any duplicates
    # Somewhat hacky solution, as we are dealing with a list of dicts
    write_data = [dict(t) for t in {tuple(d.items()) for d in write_data}]

    np.save(path, write_data)
