# Chessbot wars!

This is a simple HTTP API for chess playing agents, and a game engine that simulates a match between two agent APIs.

Agents are small flask apps. They can be run locally, and soon via Google cloud Run or Google cloud functions. The long term vision of this is that elite chess grand master algorithms will exist on the Internet, known only by their URLs, gradually getting smarter.

## Agent API format

The game engine will issue a HTTP POST to the endpoint URL with the following JSON payload:
```
{
	"game_id":"7d3a06a1-2e88-4eb3-876e-570b31cb73cd",
	"fen":"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
	"moves":["a1a2","..."],
	"turn":"white"
}
```

And returns a JSON payload with a single UCI encoded move:
```
{
	"move":"c2c4"
}
```
If no valid moves are possible, the agent should return a `null` move (however the game engine will detect this and not request a move anyway):
```
{
	"move":null
}
```

The parameter `game_id` is a unique UUID for that game, and can be used if your agent requires initialisation or state, however the example agent is stateless (the entire board being described in its fen encoding).


## Example agent

An example agent is supplied with a random move strategy. This example uses the `python-chess` module to compute the board positions from the supplied fen string, and randomly selects a valid move.

Once the agent app is running (e.g. on localhost:5000) you can curl it with:

```
curl -X POST \
	 -H 'Content-Type: application/json'\
	 -d '{"game_id":"xxx","fen":"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1","moves":[],"turn":"white"}'\
	 http://127.0.0.1:5000/move/random
```

## Quick start

Clone the repo, make a virtual env, install the requirements and run:

```
cd agent
mkvirtualenv chessbotwars-agent
pip install -r requirements.txt
python main.py
```

This will start the agent locally on port 5000. In this example we will be running a single agent process and run it against itself (its stateless), but in real life you may want more than one.

You can then run a game:

```
cd game
mkvirtualenv chessbotwars-game
pip install -r requirements.txt
python game.py --white http://127.0.0.1:5000/move/random --black http://127.0.0.1:5000/move/random
```

## Deploy to Google Cloud

You can deploy the agent (using one strategy only) to GCP cloud functions.
```
cd agent
gcloud functions deploy chessbotwarsagent --entry-point gcp_function_main --runtime python37 --trigger-http --allow-unauthenticated
```

The function `gcp_function_main` includes logic for flask routing via GCP cloud functions, so you can reach the correct strategy, e.g. `https://<project>.cloudfunctions.net/chessbotwarsagent/move/random`.