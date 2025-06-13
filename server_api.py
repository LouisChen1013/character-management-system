from flask import Flask, request, jsonify
from character_manager import CharacterManager
from monster import Monster
from player import Player

app = Flask(__name__)

server = CharacterManager("ACIT", "characters.sqlite")


# API Methods


@app.route("/server/characters", methods=["POST"])
def add_character():
    """Adds a character to the Server"""
    content = request.json

    try:
        if content["type"] == "player":
            character = Player(content["player_level"], content["job"])
        else:
            character = Monster(
                content["monster_type"], content["monster_ai_difficulty"]
            )

        server.add_character(character)

        return "", 200
    except ValueError as e:
        return str(e), 404


@app.route("/server/characters/<int:id>", methods=["GET"])
def get_character(id):
    """Gets an existing character from the Server"""
    try:
        character = server.get(id)
        return jsonify(character.to_dict()), 200
    except ValueError as e:
        return str(e), 404


@app.route("/server/characters/details/<int:id>", methods=["GET"])
def get_character_details(id):
    """Gets character details from the Server"""
    print(id)
    try:
        character = server.get_character_details(id)
        return jsonify(character), 200
    except ValueError as e:
        return str(e), 404


@app.route("/server/characters/<int:id>", methods=["DELETE"])
def delete_character(id):
    """Delete an existing character from the Server"""
    try:
        server.delete_character(id)
        return "", 200
    except ValueError as e:
        return str(e), 404


@app.route("/server/characters/all/<string:character_type>", methods=["GET"])
def get_all_by_type(character_type):
    """Gets all existing characters from the Server by type"""
    try:
        result = server.get_character_details_by_type(character_type)
        return jsonify(result), 200
    except ValueError as e:
        return str(e), 400


@app.route("/server/characters/all", methods=["GET"])
def get_all():
    """Gets all existing characters from the Server"""
    try:
        characters = server.get_all()
        character_list = [character.to_dict() for character in characters]
        return jsonify(character_list), 200
    except ValueError as e:
        return str(e), 404


@app.route("/server/characters/all_details", methods=["GET"])
def get_all_details():
    """Gets all existing characters from the Server"""
    try:
        return jsonify(server.get_all_character_details()), 200
    except ValueError as e:
        return str(e), 404


@app.route("/server/character/<int:id>", methods=["PUT"])
def update_character(id):
    """Update existing character in the Server"""
    content = request.json
    try:
        current = server.get(id)
        if current.get_type() == "player":
            server.update_character(id, content["job"], content["player_level"])
        else:
            server.update_character(
                id, content["monster_type"], content["monster_ai_difficulty"]
            )
        return "", 200
    except ValueError as e:
        return str(e), 404


@app.route("/server/serverstats", methods=["GET"])
def get_server_stats():
    """Gets server stats"""
    try:
        stats = server.get_server_stats().to_dict()
        return jsonify(stats), 200
    except ValueError as e:
        return str(e), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
