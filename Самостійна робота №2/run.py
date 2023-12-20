from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# Модель гравця
players = [
    {"id": 1, "name": "Player 1", "score": 100, "level": 5},
    {"id": 2, "name": "Player 2", "score": 150, "level": 8},
    {"id": 3, "name": "Player 3", "score": 120, "level": 6},
]

# Валідація вхідних даних
player_parser = reqparse.RequestParser()
player_parser.add_argument("name", type=str, required=True, help="Name cannot be blank")
player_parser.add_argument("score", type=int, required=True, help="Score cannot be blank")
player_parser.add_argument("level", type=int, required=True, help="Level cannot be blank")

# Ресурс для гравців
class PlayerResource(Resource):
    def get(self, player_id):
        player = next((p for p in players if p["id"] == player_id), None)
        if player:
            return player
        else:
            return {"message": "Player not found"}, 404

    def put(self, player_id):
        args = player_parser.parse_args()
        player = next((p for p in players if p["id"] == player_id), None)

        if player:
            player["name"] = args["name"]
            player["score"] = args["score"]
            player["level"] = args["level"]
            return player
        else:
            return {"message": "Player not found"}, 404

    def delete(self, player_id):
        global players
        players = [p for p in players if p["id"] != player_id]
        return {"message": "Player deleted"}

# Ресурс для всіх гравців
class PlayersResource(Resource):
    def get(self):
        return players

    def post(self):
        args = player_parser.parse_args()
        new_player = {
            "id": len(players) + 1,
            "name": args["name"],
            "score": args["score"],
            "level": args["level"]
        }
        players.append(new_player)
        return new_player, 201

# Додаємо ресурс RESTful API
api.add_resource(PlayerResource, "/api/players/<int:player_id>")
api.add_resource(PlayersResource, "/api/players")

# Початкова сторінка
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
