# Hangman — Word Studio

Repository: https://github.com/Hab1yer/hangman

Python 3.10+ is required. Install with `python -m pip install -r requirements.txt`, run `python server.py`, then open http://127.0.0.1:5000.

Run tests: `python -m unittest discover -s tests -v`. Run the keyboard regression check with `node tests/test_keyboard.cjs` (Node.js is needed only for this check).

On this Windows machine, use `.\.venv\Scripts\python.exe server.py` to run the installed environment; the system `python` alias does not work.

The independent Python engine owns all rules. Flask stores separate games by UUID. JavaScript sends guesses and renders the returned state. Active responses never contain the answer.

API: POST `/api/games` with `{"difficulty":"medium"}`; GET `/api/games/{game_id}`; POST `/api/games/{game_id}/guess` with `{"letter":"a"}`. Creation returns 201; invalid input 400; missing game 404; duplicate or post-game guess 409. JSON errors contain `error`.

Deploy: push to your GitHub repository, then create a Render Blueprint using render.yaml. Alternatively use build command `pip install -r requirements.txt` and start command `gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 server:app`. Use one worker because games live in memory. Restart clears games; the oldest game is evicted at 10,000 games.

Deployment and manual browser verification remain pending. Complete a game at the public HTTPS URL, start another, and inspect a guess request and JSON response in browser developer tools. Prepare your report and recording based on your actual experience.

Scope follows the assignment: terminal clients, bots, evaluations and leaderboards are excluded.
