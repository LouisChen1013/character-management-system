from flask import Flask, request
import json
from character_manager import CharacterManager
from monster import Monster
from player import Player

app = Flask(__name__)

server = CharacterManager("ACIT", "characters.sqlite")


# API Methods

@app.route('/server/characters', methods=['POST'])
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

        response = app.response_class(status=200)
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


@app.route('/server/characters/details/<int:id>', methods=['GET'])
def get_character_details(id):
    """ Gets character details from the Server """
    try:
        character = server.get_character_details(id)
        response = app.response_class(
            status=200,
            response=json.dumps(
                character
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
        characters = server.get_all()

        character_list = []

        for character in characters:
            character = character.to_dict()
            character_list.append(character)
        response = app.response_class(
            status=200,
            response=json.dumps(
                character_list
            ),
            mimetype='application/json'
        )
        return response
    except ValueError as e:
        response = app.response_class(response=str(e), status=404)
        return response


@app.route('/server/characters/all_details', methods=['GET'])
def get_all_details():
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
            character = server.update_character(id,
                                                content["job"], content["player_level"])
        else:
            character = server.update_character(
                id, content["monster_type"], content["monster_ai_difficulty"])
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
