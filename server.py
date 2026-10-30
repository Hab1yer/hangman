from pathlib import Path
from secrets import choice
from uuid import uuid4
from threading import RLock
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from game import HangmanGame

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4096
games = {}
lock = RLock()

@app.errorhandler(HTTPException)
def http_error(e): return jsonify(error=e.description), e.code

@app.errorhandler(ValueError)
def invalid(e): return jsonify(error=str(e)), 400

@app.errorhandler(RuntimeError)
def conflict(e): return jsonify(error=str(e)), 409

def body(key):
    data = request.get_json()
    if not isinstance(data, dict) or set(data) != {key}: raise ValueError('Expected JSON field: ' + key)
    return data[key]

@app.get('/')
def home(): return app.send_static_file('index.html')

@app.post('/api/games')
def create():
    difficulty = body('difficulty')
    if not isinstance(difficulty, str) or difficulty not in ('easy','medium','hard'): raise ValueError('Choose easy, medium, or hard.')
    words = (Path(__file__).parent / 'words' / (difficulty+'.txt')).read_text().split()
    with lock:
        if len(games) >= 10000: games.pop(next(iter(games)))
        game_id = uuid4().hex
        games[game_id] = HangmanGame(choice(words), difficulty)
        return jsonify(game_id=game_id, **games[game_id].state()), 201

@app.get('/api/games/<game_id>')
@app.post('/api/games/<game_id>/guess')
def action(game_id):
    with lock:
        if game_id not in games: return jsonify(error='Game not found. Start a new game.'), 404
        game = games[game_id]
        if request.method == 'POST': game.guess(body('letter'))
        return jsonify(game_id=game_id, **game.state())

if __name__ == '__main__': app.run(port=5000)
