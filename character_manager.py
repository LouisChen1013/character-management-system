from unittest.mock import patch, mock_open
from abstract_character import AbstractCharacter
from player import Player
from monster import Monster
from server_stats import ServerStats
import os.path
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class CharacterManager:
    """ This is the Character Manager class """

    CHARACTER_LABEL = "Server Name"
    ID_LABEL = "ID"
    DB_NAME_LABEL = "Database Name"
    JOB_TYPE_LABEL = "Job/Type"
    LEVEL_LABEL = "Level"
    DIFFICULTY_LABEL = "Difficulty"

    def __init__(self, server_name, db_filename):
        """ Constructor - Initialize main attribute of CharacterManager """

        CharacterManager._validate_string_input(
            CharacterManager.CHARACTER_LABEL, server_name)
        if server_name is None or not isinstance(server_name, str):
            raise ValueError("Server Name must be string")

        CharacterManager._validate_string_input(
            CharacterManager.DB_NAME_LABEL, db_filename)
        if db_filename is None or not isinstance(db_filename, str):
            raise ValueError("Database Name must be string")

        engine = create_engine('sqlite:///' + db_filename)
        self._db_session = sessionmaker(bind=engine)

        self._db_filename = db_filename
        self._server_name = server_name

    def add_character(self, character_obj):
        """ Adds character object to character list if it is not on the list """

        if character_obj is None:
            raise ValueError("Character Object cannot be undefined")
        if character_obj == "":
            raise ValueError("Character Object cannot be empty")
        if not isinstance(character_obj, AbstractCharacter):
            raise ValueError("Invalid Character Object")

        session = self._db_session()
        session.add(character_obj)
        session.commit()
        session.close()

    def character_exists(self, id):
        """ Checks if character already exists in character list """

        CharacterManager._validate_string_input(CharacterManager.ID_LABEL, id)
        CharacterManager._validate_int_id(CharacterManager.ID_LABEL, id)

        session = self._db_session()
        character = session.query(AbstractCharacter).filter(
            AbstractCharacter.id == id).first()
        session.close()

        if character is not None:
            return True

        return False

    def get(self, id):
        """ get – Takes in an ID and returns that entity object from the list of entities, if it exists. Returns None if it does not exist. """

        CharacterManager._validate_string_input(CharacterManager.ID_LABEL, id)
        CharacterManager._validate_int_id(CharacterManager.ID_LABEL, id)
        session = self._db_session()

        if self.character_exists(id):
            character = session.query(Player).filter(
                Player.type == "player", Player.id == id).first()
            if character is None:
                character = session.query(Monster).filter(
                    Monster.type == "monster", Monster.id == id).first()
        else:
            raise ValueError("Character ID does not exist")

        session.close()
        return character

    def get_all(self):
        """ Returns a list of all characters """
        session = self._db_session()
        characters = characters = session.query(Player).filter(
            Player.type == "player").all() + session.query(Monster).filter(
            Monster.type == "monster").all()
        session.close()
        return characters

    def get_all_by_type(self, character_type):
        """ Returns character list by type """

        if character_type is None or character_type not in ["player", "monster"]:
            raise ValueError(
                "Character type must be either player or monster")

        session = self._db_session()

        if character_type == Player.CHARACTER_TYPE:
            characters = session.query(Player).filter(
                Player.type == "player").all()
        elif character_type == Monster.CHARACTER_TYPE:
            characters = session.query(Monster).filter(
                Monster.type == "monster").all()
        else:
            characters = []

        session.close()
        return characters

    def update_character(self, id, job_type, level_difficulty):
        """ Update character – Takes in an entity object and replaces the existing entity in the list of entities based on the ID. """

        # Raises an exception if an entity with the same ID does not exist in the list of entities.
        CharacterManager._validate_string_input(CharacterManager.ID_LABEL, id)
        CharacterManager._validate_int_id(CharacterManager.ID_LABEL, id)

        CharacterManager._validate_string_input(
            CharacterManager.JOB_TYPE_LABEL, job_type)

        session = self._db_session()

        if self.character_exists(id):
            character = session.query(AbstractCharacter).filter(
                AbstractCharacter.id == id).first()
            if character.type == "player":
                CharacterManager._validate_int_id(
                    CharacterManager.LEVEL_LABEL, level_difficulty)
                character = session.query(Player).filter(
                    Player.type == "player", Player.id == id).first()
                character.set_job(job_type)
                character.set_level(level_difficulty)
            else:
                CharacterManager._validate_string_input(
                    CharacterManager.DIFFICULTY_LABEL, level_difficulty)
                character = session.query(Monster).filter(
                    Monster.type == "monster", Monster.id == id).first()
                character.set_monster_type(job_type)
                character.set_monster_ai_difficulty(level_difficulty)
        else:
            raise ValueError("Character ID does not exist")

        session.commit()

        session.close()

    def delete_character(self, id):
        """ Delete existing character from character list """

        CharacterManager._validate_string_input(
            CharacterManager.ID_LABEL, id)
        CharacterManager._validate_int_id(CharacterManager.ID_LABEL, id)

        session = self._db_session()

        character = session.query(AbstractCharacter).filter(
            AbstractCharacter.id == id).first()

        if character is None:
            session.close()
            raise ValueError("Character does not exist")

        session.delete(character)
        session.commit()
        session.close()

    def get_server_name(self):
        """ Returns server name """

        return self._server_name

    def get_server_stats(self):
        """ Returns a ServerStats object """

        session = self._db_session()
        characters = self.get_all_by_type(
            "player") + self.get_all_by_type("monster")
        session.close()

        total_num_characters = len(characters)
        avg_player_level = 0
        total_player_level = 0
        avg_monster_ai_difficulty = 0
        total_monster_level = 0
        num_players = len(self.get_all_by_type("player"))
        num_monsters = len(self.get_all_by_type("monster"))

        for curr_character in characters:
            if curr_character.type == Player.CHARACTER_TYPE:
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

    def get_character_details(self, id):
        """ Returns character details """

        CharacterManager._validate_string_input(CharacterManager.ID_LABEL, id)
        CharacterManager._validate_int_id(CharacterManager.ID_LABEL, id)

        details = self.get(id).get_full_details()

        return details

    def get_character_details_by_type(self, character_type):
        """ Returns a list of details for the given character type """

        if character_type is None or (character_type != Player.CHARACTER_TYPE and character_type != Monster.CHARACTER_TYPE):
            raise ValueError("Invalid character type")

        session = self._db_session()

        if character_type == Player.CHARACTER_TYPE:
            characters = session.query(Player).filter(
                Player.type == "player").all()
        elif character_type == Monster.CHARACTER_TYPE:
            characters = session.query(Monster).filter(
                Monster.type == "monster").all()
        else:
            characters = []

        session.close()

        character_detail_list = []

        for curr_character in characters:
            character_detail_list.append(curr_character.get_details())

        return character_detail_list

    def get_all_character_details(self):
        """ Returns a list of details for the all character """

        session = self._db_session()
        characters = self.get_all()
        session.close()

        character_detail_list = []

        for curr_character in characters:
            character_detail_list.append(curr_character.get_details())

        return character_detail_list

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
