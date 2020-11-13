import chess
import random
import argparse
import uuid
import requests

SPACER_STR = "==============="
RESULT_DESCRIPTIONS = {
    "1/2-1/2": "Draw",
    "1-0": "White wins",
    "0-1": "Black wins"
}

parser = argparse.ArgumentParser(
    description='Simular a chess game using remove agent APIs.'
    )
parser.add_argument('--white',
    type=str,
    help='white player agent URL'
    )
parser.add_argument('--black',
    type=str,
    help='black player agent URL'
    )
parser.add_argument('--pause',
    help='pause between each move (default false)',
    default=False,
    action='store_true'
    )
args = parser.parse_args()

white_agent_url = args.white
black_agent_url = args.black

game_id = str(uuid.uuid4())
board = chess.Board()
moves = []

def process_move(turn, board, agent_url):
    request_body = {
        "game_id": game_id,
        "turn": turn,
        "fen": board.fen(),
        "moves":moves
    }
    resp = requests.post(url=agent_url, json=request_body).json()
    print(resp)
    legal_moves = list(board.legal_moves)
    random.shuffle(legal_moves)
    move_uci = legal_moves[0].uci()
    board.push_uci(move_uci)
    return move_uci

def print_move(turn, board, move_uci):
    print()
    print(SPACER_STR)
    print('#%s %s' % (len(moves), turn))
    print(move_uci)
    print(board)

print("Game: %s" % game_id)
while True:
    turn = 'white'
    move_uci = process_move(turn, board, white_agent_url)
    moves.append(move_uci)
    print_move(turn, board, move_uci)

    if board.is_game_over():
        break;

    turn = 'black'
    move_uci = process_move(turn, board, black_agent_url)
    moves.append(move_uci)
    print_move(turn, board, move_uci)

    if board.is_game_over():
        break;

    if args.pause:
        input("Press Enter to continue...")

print()
print(SPACER_STR)
print("== Game over ==")
print(board)

result_str = board.result()
result_description = RESULT_DESCRIPTIONS[result_str]
print("Result: %s (%s)" % (result_str, result_description))
print("Checkmate: %s" % board.is_checkmate())
print("Stalemate: %s" % board.is_stalemate())
print("Insufficent Material: %s" % board.is_insufficient_material())
print("Moves:")
print(moves)