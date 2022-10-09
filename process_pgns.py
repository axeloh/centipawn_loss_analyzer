import chess
import chess.engine
import chess.pgn
import numpy as np
import time
import multiprocessing as mp
import logging 

from helpers import read_games, parse_elo_rating, evaluate_position

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("logs/debug.log"),
        logging.StreamHandler()
    ])

STOCKFISH_PATH = '/usr/local/Cellar/stockfish/15/bin/stockfish'
ENGINE = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
MOVETIMESEC = 999
DEPTH = 15
LIMIT = chess.engine.Limit(time=MOVETIMESEC, depth=DEPTH)

DATA_PATH = 'data' 
OUTPUT_PATH = 'processed_data'

INCLUDE_PLAYERS = [
    'Anand', 
    'Aronian', 
    'Carlsen', 
    'Caruana', 
    'Ding', 
    'Duda', 
    'So', 
    'PolgarJ', 
    'Nepo', 
    'Jobava', 
    'Firouzja', 
    'Niemann',
    'Pragg',
    'Gukesh',
    'Erigaisi',
    'Keymer',
    'Sarin'
    ]

MAX_NUM_GAMES_PER_PLAYER = 500

# evaluator = Evaluator(ENGINE, LIMIT)

def process_player_games(player_name: str) -> None:
    logging.info(f'-- Processing games for player: {player_name}')
    
    output = []
    try:
        pgn_path = f'{DATA_PATH}/{player_name}.pgn'
        games = read_games(pgn_path)
    except Exception as _:
        logging.error(f'[{player_name}] Couldnt read games.')
        return 

    for i, game in enumerate(games, start=1):
        if i > MAX_NUM_GAMES_PER_PLAYER:
            break
        
        # Save every now and then
        if i % (min(MAX_NUM_GAMES_PER_PLAYER, len(games)) // 5) == 0:
            np.save(f'{OUTPUT_PATH}/{player_name}.npy', output)
            logging.info(f'[{player_name}] Saved after {i} games.')

        try: 
            logging.info(f'[{player_name}] Game: {i}/{len(games)}')
            event = game.headers['Event']
            date = game.headers['Date']
            white_player = game.headers['White']
            black_player = game.headers['Black']
            white_elo = parse_elo_rating(game.headers['WhiteElo'])
            black_elo = parse_elo_rating(game.headers['BlackElo'])
            result = game.headers['Result']

            if white_elo is None and black_elo is None:
                continue

            board = game.board()
            # init_evaluation = evaluator.evaluate(board.fen())
            init_evaluation = evaluate_position(board, ENGINE, LIMIT)
            evaluations = [init_evaluation]
            moves = game.mainline_moves()
            for move in moves:
                board.push(move)
                # position_evaluation = evaluator.evaluate(board.fen()) 
                position_evaluation = evaluate_position(board, ENGINE, LIMIT)
                evaluations.append(position_evaluation)

            evaluations = np.array(evaluations)
            evaluations[evaluations < -1000] = -1000
            evaluations[evaluations > 1000] = 1000

            white_centipawn_losses = -np.diff(evaluations)[::2]
            black_centipawn_losses  = np.diff(evaluations)[1::2]
            white_centipawn_losses[white_centipawn_losses < 0] = 0
            black_centipawn_losses[black_centipawn_losses < 0] = 0

            avg_white_cp_loss = np.mean(white_centipawn_losses)
            avg_black_cp_loss = np.mean(black_centipawn_losses)

            game_output = {
                'event': event,
                'date': date,
                'white_player': white_player,
                'black_player': black_player,
                'white_elo': white_elo,
                'black_elo': black_elo,
                'result': result,
                'avg_white_cp_loss': avg_white_cp_loss,
                'avg_black_cp_loss': avg_black_cp_loss,
                'white_cp_losses': white_centipawn_losses,
                'black_cp_losses': black_centipawn_losses,
            }
            output.append(game_output)
        except Exception as exc:
            logging.error(f'[{player_name}] Couldnt process game: {i}.')         

    if len(output) == 0:
        logging.warning(f'[{player_name}] No relevant games.')
        return 

    np.save(f'{OUTPUT_PATH}/{player_name}.npy', output)
    logging.info(f'--Done for player: {player_name}')


if __name__ == '__main__':
    logging.info('Starting processing pgns.. ')
    start_time = time.time()

    # Parallelize 
    with mp.Pool(mp.cpu_count()) as pool:
        pool.map(process_player_games, INCLUDE_PLAYERS)

    end_time = time.time()
    logging.info(f'---- Done for all players in {(end_time-start_time):.2f}s.')
