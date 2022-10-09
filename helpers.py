import chess
import chess.engine
import chess.pgn
from typing import Callable, Union, List
from datetime import datetime
import time
from functools import wraps

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

def is_classical(event: str):
    return 'blitz' not in event.lower() and 'rapid' not in event.lower()



def timing(func: Callable):
    """Decorator to time any function."""
    @wraps(func)
    def wrap(*args, **kw):
        ts = time.time()
        result = func(*args, **kw)
        te = time.time()
        print(f'{func.__name__} done in {(te-ts):.3f}s.')
        return result
    return wrap