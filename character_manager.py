from unittest.mock import patch, mock_open
from abstract_character import AbstractCharacter
from player import Player
from monster import Monster
from server_stats import ServerStats
import os.path
import json


class CharacterManager:
    """ This is the Character Manager class """

    CHARACTER_LABEL = "Server Name"
    ID_LABEL = "ID"
    FILEPATH_LABEL = "Filepath"

    def __init__(self, server_name, filepath):
        """ Constructor - Initialize main attribute of CharacterManager """

        CharacterManager._validate_string_input(
            CharacterManager.CHARACTER_LABEL, server_name)
        if server_name is None or not isinstance(server_name, str):
            raise ValueError("Server Name must be string")

        CharacterManager._validate_string_input(
            CharacterManager.FILEPATH_LABEL, filepath)
        if filepath is None or not isinstance(filepath, str):
            raise ValueError("Filepath must be string")

        self._server_name = server_name
        self._next_available_id = int(0)
        self._character_list = []
        self._filepath = filepath
        self._read_entities_from_file()

    def add_character(self, character_obj):
        """ Adds character object to character list if it is not on the list """

        if character_obj is None:
            raise ValueError("Character Object cannot be undefined")
        if character_obj is "":
            raise ValueError("Character Object cannot be empty")
        if not isinstance(character_obj, AbstractCharacter):
            raise ValueError("Invalid Character Object")

        if character_obj not in self._character_list:
            self._next_available_id = self._next_available_id + 1
            character_obj.set_id(self._next_available_id)
            self._character_list.append(character_obj)
        self._write_entities_to_file()
        return self._next_available_id

    def get_assigned_id(self):
        """ Get assigned id """

        return self._next_available_id

    def character_exists(self, id):
        """ Checks if character already exists in character list """

        CharacterManager._validate_string_input(CharacterManager.ID_LABEL, id)
        CharacterManager._validate_int_id(CharacterManager.ID_LABEL, id)

        for character in self._character_list:
            if character.get_id() == id:
                return True
        return False

    def get(self, id):
        """ get – Takes in an ID and returns that entity object from the list of entities, if it exists. Returns None if it does not exist. """

        CharacterManager._validate_string_input(CharacterManager.ID_LABEL, id)
        CharacterManager._validate_int_id(CharacterManager.ID_LABEL, id)

        for character in self._character_list:
            if character.get_id() == id:
                return character
        raise ValueError("Character does not exist")

    def get_all(self):
        """ Returns a list of all characters """

        return self._character_list

    def get_all_by_type(self, character_type):
        """ Returns character list by type """

        if character_type is None or character_type not in ["player", "monster"]:
            raise ValueError(
                "Character_type type must be either player or monster")
        character_type_list = []
        for character in self._character_list:
            if character.get_type() == character_type:
                character_type_list.append(character)
        return character_type_list

    def update_character(self, character_obj):
        """ Update character  Update – Takes in an entity object and replaces the existing entity in the list of entities based on the ID. """

        # Raises an exception if an entity with the same ID does not exist in the list of entities.

        if character_obj is None:
            raise ValueError("Character Object cannot be undefined")
        if character_obj is "":
            raise ValueError("Character Object cannot be empty")
        if not isinstance(character_obj, AbstractCharacter):
            raise ValueError("Invalid Character Object")

        character_id = character_obj.get_id()

        if self.character_exists(character_id) is False:
            raise Exception("Character ID does not exist")
        for i, character in enumerate(self._character_list, 0):
            if character.get_id() == character_id:
                self._character_list[i] = character_obj
                self._write_entities_to_file()
                break

    def delete_character(self, id):
        """ Delete existing character from character list """

        CharacterManager._validate_string_input(
            CharacterManager.ID_LABEL, id)
        CharacterManager._validate_int_id(CharacterManager.ID_LABEL, id)

        for character in self._character_list:
            if character.get_id() == id:
                self._character_list.remove(character)
                self._write_entities_to_file()
                return
        raise ValueError("Character does not exist.")

    def get_server_name(self):
        """ Returns server name """

        return self._server_name

    def get_server_stats(self):
        """ Returns a ServerStats object """

        total_num_characters = len(self._character_list)
        avg_player_level = 0
        total_player_level = 0
        avg_monster_ai_difficulty = 0
        total_monster_level = 0
        num_players = len(self.get_all_by_type("player"))
        num_monsters = len(self.get_all_by_type("monster"))

        for curr_character in self._character_list:
            if curr_character.get_type() == "player":
                total_player_level += curr_character.get_level()
            else:
                if curr_character.get_monster_ai_difficulty() == "easy":
                    total_monster_level += 1
                elif curr_character.get_monster_ai_difficulty() == "normal":
                    total_monster_level += 2
                elif curr_character.get_monster_ai_difficulty() == "hard":
                    total_monster_level += 3
        if num_players != 0:
            avg_player_level = int(total_player_level / num_players)
        else:
            avg_player_level = 0

        if num_monsters != 0:
            avg_monster_ai_difficulty = total_monster_level / num_monsters
        else:
            avg_monster_ai_difficulty = 0

        if avg_monster_ai_difficulty == 0:
            avg_monster_ai_difficulty = "not available"
        elif round(avg_monster_ai_difficulty) == 1:
            avg_monster_ai_difficulty = "easy"
        elif round(avg_monster_ai_difficulty) == 2:
            avg_monster_ai_difficulty = "normal"
        else:
            avg_monster_ai_difficulty = "hard"

        return ServerStats(total_num_characters, num_monsters, num_players, avg_player_level, avg_monster_ai_difficulty)

    def get_character_details_by_type(self, character_type):
        """ Returns a list of details for the given character type """

        if character_type is None or (character_type != Player.CHARACTER_TYPE and character_type != Monster.CHARACTER_TYPE):
            raise ValueError("Invalid character type")

        character_detail_list = []

        for curr_character in self._character_list:
            if curr_character.get_type() == character_type:
                character_detail_list.append(curr_character.get_details())

        return character_detail_list

    def get_all_character_details(self):
        """ Returns a list of details for the all character """

        character_detail_list = []

        for curr_character in self._character_list:
            character_detail_list.append(curr_character.get_details())

        return character_detail_list

    def _read_entities_from_file(self):
        """ Read entities from text file"""

        if os.path.isfile(os.path.basename(self._filepath) + '.txt'):
            with open(os.path.basename(self._filepath) + '.txt', "r") as file:
                if os.stat(os.path.basename(self._filepath) + '.txt').st_size == 0:
                    return
                else:
                    character_dict = json.load(file)
                    for char in character_dict:
                        if char["type"] == "player":
                            character = Player(
                                char['player_level'], char['job'])
                        elif char["type"] == "monster":
                            character = Monster(
                                char['monster_type'], char['monster_ai_difficulty'])

                        else:
                            raise ValueError("Character type is not supported")
                        character.set_id(char['id'])
                        self.add_character(character)
        else:
            raise ValueError(
                "This file does not exist, create one before running")

    def _write_entities_to_file(self):
        """ Write entities to text file """

        with open(os.path.basename(self._filepath) + '.txt', 'r+') as file:
            data_list = []

            for character in self._character_list:
                data_list.append(character.to_dict())

            json.dump(data_list, file)

    @staticmethod
    def _validate_string_input(display_name, str_value):
        """ Private helper to validate string values """

        if str_value is None:
            raise ValueError(display_name + " cannot be undefined.")

        if str_value == "":
            raise ValueError(display_name + " cannot be empty.")

    @staticmethod
    def _validate_int_id(display_name, id):
        """ Private helper to validate integer id """

        if type(id) != int:
            raise ValueError(display_name + " needs to be integer")
