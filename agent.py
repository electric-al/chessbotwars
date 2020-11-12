from flask import Flask, request, jsonify
import chess
import random
import os

app = Flask(__name__)

def random_move_strategy(game_id, board, moves):
    legal_moves = list(board.legal_moves)
    random.shuffle(legal_moves)
    return legal_moves[0]

def handle_move_request(requst, fn):
    body = request.json
    game_id = body['game_id']
    fen = body['fen']
    moves = body['moves']
    board = chess.Board(fen)
    move = fn(game_id, board, moves)
    return jsonify({"move":move.uci()})

@app.route('/')
@app.route('/index')
def index():
    return "Hello, chessbot!"

# Add more engines here
# @app.route('/move/<whatever>', methods=['POST'])

@app.route('/move/random', methods=['POST'])
def move():
    return handle_move_request(request, random_move_strategy)

port = int(os.environ.get('PORT', 5000))
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=port)