from flask import Flask, request, jsonify
import chess
import random
import os
import werkzeug.datastructures

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

# GCP cloud function entry point
# Dispatches a flask request to the app application
def gcp_function_main(request):
    with app.app_context():
        headers = werkzeug.datastructures.Headers()
        for key, value in request.headers.items():
            headers.add(key, value)
        with app.test_request_context(method=request.method, base_url=request.base_url, path=request.path, query_string=request.query_string, headers=headers, data=request.data):
            try:
                rv = app.preprocess_request()
                if rv is None:
                    rv = app.dispatch_request()
            except Exception as e:
                rv = app.handle_user_exception(e)
            response = app.make_response(rv)
            return app.process_response(response)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)