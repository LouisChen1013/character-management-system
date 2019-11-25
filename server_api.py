from flask import Flask, request
import json
from character_manager import CharacterManager
from monster import Monster
from player import Player

app = Flask(__name__)

server = CharacterManager("ACIT", "/Users/QB/Desktop/Pure_Python/Assignment2")


# API Methods

@app.route('/server/character', methods=['POST'])
def add_character():
    """ Adds a character to the Server """
    content = request.json
    try:
        if content['type'] == "player":
            character = Player(content['player_level'], content['job'])
            server.add_character(character)
        else:
            character = Monster(content['monster_type'],
                                content['monster_ai_difficulty'])
            server.add_character(character)

        response = app.response_class(
            status=200,
            response=json.dumps(
                server.get_assigned_id()
            ), mimetype='application/json'
        )
    except ValueError as e:
        response = app.response_class(
            response=str(e),
            status=400
        )
    return response


@app.route('/server/characters/<int:id>', methods=['GET'])
def get_character(id):
    """ Gets an existing character from the Server """
    try:
        character = server.get(id)
        response = app.response_class(
            status=200,
            response=json.dumps(
                character.to_dict()
            ),
            mimetype='application/json'
        )
        return response
    except ValueError as e:
        response = app.response_class(response=str(e), status=404)
        return response


@app.route('/server/characters/<int:id>', methods=['DELETE'])
def delete_character(id):
    """ Delete an existing character from the Server """
    try:
        character = server.delete_character(id)
        response = app.response_class(status=200)
        return response

    except ValueError as e:
        response = app.response_class(
            response=str(e),
            status=404
        )
    return response


@app.route('/server/characters/all/<string:character_type>', methods=['GET'])
def get_all_by_type(character_type):
    """ Gets all existing characters from the Server by type """
    try:
        response = app.response_class(
            status=200,
            response=json.dumps(
                server.get_character_details_by_type(character_type)
            ),
            mimetype='application/json'
        )
        return response
    except ValueError as e:
        response = app.response_class(response=str(e), status=400)
        return response


@app.route('/server/characters/all', methods=['GET'])
def get_all():
    """ Gets all existing characters from the Server """
    try:
        response = app.response_class(
            status=200,
            response=json.dumps(
                server.get_all_character_details()
            ),
            mimetype='application/json'
        )
        return response
    except ValueError as e:
        response = app.response_class(response=str(e), status=404)
        return response


@app.route('/server/character/<int:id>', methods=['PUT'])
def update_character(id):
    """ Update existing character in the Server """
    content = request.json
    try:
        if server.get(id).get_type() == "player":
            if content.keys() >= {"job", "player_level"}:
                character = server.get(id).set_job(content["job"])
                character = server.get(id).set_level(content["player_level"])
                response = app.response_class(status=200)
            elif "player_level" in content:
                character = server.get(id).set_level(content["player_level"])
                response = app.response_class(status=200)
            else:
                character = server.get(id).set_job(content["job"])
                response = app.response_class(status=200)
        else:
            if content.keys() >= {"monster_ai_difficulty", "monster_type"}:
                character = server.get(id).set_monster_ai_difficulty(
                    content["monster_ai_difficulty"])
                character = server.get(id).set_monster_type(
                    content["monster_type"])
                response = app.response_class(status=200)
            elif "monster_ai_difficulty" in content:
                character = server.get(
                    id).set_monster_ai_difficulty(content["monster_ai_difficulty"])
                response = app.response_class(status=200)
            else:
                character = server.get(id).set_monster_type(
                    content["monster_type"])
                response = app.response_class(status=200)

    except ValueError as e:
        response = app.response_class(
            response=str(e),
            status=404
        )
    return response


@app.route('/server/serverstats', methods=['GET'])
def get_server_stats():
    """ Gets server stats """
    try:
        response = app.response_class(status=200, response=json.dumps(
            server.get_server_stats().to_dict()), mimetype='application/json')
        return response
    except ValueError as e:
        response = app.response_class(response=str(e), status=404)
        return response


if __name__ == "__main__":
    app.run()
