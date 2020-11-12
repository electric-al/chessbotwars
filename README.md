# Chessbot wars!

This is a simple http API for chess playing agents, and a game engine that simulates a match between two agent APIs.

Agents are small flask apps. They can be run locally, and soon via Google cloud Run or Google cloud functions. The long term vision of this is that elite chess grand master algoriths will exist on the Internet, known only by their URLs, gradually getting smarter.

## Argent API format

The game engine will issue a HTTP POST to the endpoint URL with the following JSON payload:
```
{
	"game_id":"7d3a06a1-2e88-4eb3-876e-570b31cb73cd",
	"fen":"8/ppppppPp/8/8/8/8/8/8 w KQkq - 0 1",
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

## Example agent

An example agent is supplied with a random move stratgy. This example uses the `python-chess` module to compute the board positions from the supplied fen string, and randomly selects a valid move.

Once the agent app is running (e.g. on localhost:5000) you can curl it with:

```
curl -X POST \
	 -H 'Content-Type: application/json'\
	 -d '{"game_id":4,"fen":"8/ppppppPp/8/8/8/8/8/8 w KQkq - 0 1","moves":[],"turn":"white"}'\
	 http://127.0.0.1:5000/move/random
```

## Quick start

Clone the repo, make a virtual env (`mkvirtualenv chessbotwars`) and install the requirements.

Run the agent:

```
python agent.py
```

This will start the agent locally on port 5000. In this example we will be running a single agent process and run it against itself (its stateless), but in real life you may want more than one.

You can then run a game:

```
python game.py --white http://127.0.0.1:5000/move/random --black http://127.0.0.1:5000/move/random
```