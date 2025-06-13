from abstract_character import AbstractCharacter
from player import Player
from monster import Monster
from server_stats import ServerStats

from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session


class CharacterManager:
    """Manages character data (Players and Monsters) on a server,
    providing CRUD operations and server statistics."""

    SERVER_NAME_LABEL = "Server Name"
    ID_LABEL = "ID"
    DB_NAME_LABEL = "Database Name"
    JOB_TYPE_LABEL = "Job/Type"
    LEVEL_LABEL = "Level"
    DIFFICULTY_LABEL = "Difficulty"

    def __init__(self, server_name: str, db_filename: str, engine: Engine = None):
        """
        Constructor - Initializes the CharacterManager with a server name
        and sets up the database connection.
        """

        # Validate server_name
        self._validate_non_empty_string(self.SERVER_NAME_LABEL, server_name)
        if not isinstance(server_name, str):
            raise ValueError("Server Name must be a string.")
        self._server_name = server_name

        # Validate db_filename
        self._validate_non_empty_string(self.DB_NAME_LABEL, db_filename)
        if not isinstance(db_filename, str):
            raise ValueError("Database Name must be a string.")
        self._db_filename = db_filename

        if engine:
            self._engine = engine
        else:
            self._engine = create_engine(f"sqlite:///{db_filename}")
        self._db_session_factory = sessionmaker(bind=self._engine)

    def _validate_non_empty_string(self, display_name: str, value):
        """Private helper to validate that a value is a non-empty string."""

        if value is None:
            raise ValueError(f"{display_name} cannot be undefined (None).")
        if not isinstance(value, str):
            raise ValueError(f"{display_name} must be a string.")
        if value == "":
            raise ValueError(f"{display_name} cannot be empty.")

    def _validate_integer_id(self, display_name: str, id_value):
        """Private helper to validate that an ID is an integer."""

        if id_value is None:
            raise ValueError(f"{display_name} cannot be undefined (None).")
        if id_value == "":
            raise ValueError(f"{display_name} cannot be empty.")
        if not isinstance(id_value, int):
            raise ValueError(f"{display_name} needs to be an integer.")

    def add_character(self, character_obj: AbstractCharacter):
        """Adds a character object to the database."""

        if character_obj is None:
            raise ValueError("Character Object cannot be undefined.")
        if not isinstance(character_obj, AbstractCharacter):
            raise ValueError(
                "Invalid Character Object: Must be an instance of AbstractCharacter or its subclass."
            )

        with self._db_session_factory() as session:
            session.add(character_obj)
            session.flush()
            session.commit()

    def character_exists(self, char_id: int) -> bool:
        """Checks if a character with the given ID exists in the database."""

        self._validate_integer_id(self.ID_LABEL, char_id)

        with self._db_session_factory() as session:
            character = session.execute(
                select(AbstractCharacter).filter(AbstractCharacter.id == char_id)
            ).scalar_one_or_none()

        return character is not None

    def get(self, char_id: int) -> AbstractCharacter:
        """
        Retrieves a character object by ID from the database.
        Attempts to load as Player then Monster if type is ambiguous.
        """

        self._validate_integer_id(self.ID_LABEL, char_id)

        with self._db_session_factory() as session:
            character = session.execute(
                select(Player).filter(Player.id == char_id)
            ).scalar_one_or_none()

            if character is None:
                character = session.execute(
                    select(Monster).filter(Monster.id == char_id)
                ).scalar_one_or_none()

        if character is None:
            raise ValueError(f"Character with ID {char_id} does not exist.")

        return character

    def get_all(self) -> list[AbstractCharacter]:
        """Returns a list of all characters (Players and Monsters) in the database."""

        with self._db_session_factory() as session:
            players = session.execute(select(Player)).scalars().all()
            monsters = session.execute(select(Monster)).scalars().all()
            characters = players + monsters
        return characters

    def get_all_by_type(self, character_type: str) -> list[AbstractCharacter]:
        """Returns a list of characters filtered by type ('player' or 'monster')."""

        self._validate_non_empty_string("Character type", character_type)
        if character_type not in [Player.CHARACTER_TYPE, Monster.CHARACTER_TYPE]:
            raise ValueError("Character type must be either 'player' or 'monster'.")

        with self._db_session_factory() as session:
            if character_type == Player.CHARACTER_TYPE:
                characters = session.execute(select(Player)).scalars().all()
            elif character_type == Monster.CHARACTER_TYPE:
                characters = session.execute(select(Monster)).scalars().all()
            else:
                characters = []
        return characters

    def update_character(
        self, char_id: int, type_specific_param1, type_specific_param2
    ):
        """
        Updates an existing character's job/type and level/difficulty.
        The exact parameters (job_type, level_difficulty) depend on the character's type.
        """

        self._validate_integer_id(self.ID_LABEL, char_id)

        character = self.get(char_id)

        with self._db_session_factory() as session:
            if character.type == Player.CHARACTER_TYPE:
                self._validate_non_empty_string(
                    self.JOB_TYPE_LABEL, type_specific_param1
                )
                self._validate_integer_id(self.LEVEL_LABEL, type_specific_param2)
                player = session.get(Player, char_id)
                player.set_job(type_specific_param1)
                player.set_level(type_specific_param2)

            elif character.type == Monster.CHARACTER_TYPE:
                self._validate_non_empty_string(
                    self.JOB_TYPE_LABEL, type_specific_param1
                )
                self._validate_non_empty_string(
                    self.DIFFICULTY_LABEL, type_specific_param2
                )
                monster = session.get(Monster, char_id)
                monster.set_monster_type(type_specific_param1)
                monster.set_monster_ai_difficulty(type_specific_param2)
            else:
                raise ValueError("Unsupported character type for update.")

            session.commit()

    def delete_character(self, char_id: int):
        """Deletes an existing character from the database by ID."""

        self._validate_integer_id(self.ID_LABEL, char_id)

        with self._db_session_factory() as session:
            character = session.execute(
                select(AbstractCharacter).filter(AbstractCharacter.id == char_id)
            ).scalar_one_or_none()

            if character is None:
                raise ValueError(f"Character with ID {char_id} does not exist.")

            session.delete(character)
            session.commit()

    def get_server_name(self) -> str:
        """Returns the server name."""

        return self._server_name

    def get_server_stats(self) -> ServerStats:
        """Calculates and returns a ServerStats object based on current character data."""

        all_players = self.get_all_by_type("player")
        all_monsters = self.get_all_by_type("monster")
        characters = all_players + all_monsters

        total_num_characters = len(characters)
        num_players = len(all_players)
        num_monsters = len(all_monsters)

        total_player_level = 0
        total_monster_difficulty_value = 0

        for char in characters:
            if char.type == Player.CHARACTER_TYPE:
                total_player_level += char.get_level()
            elif char.type == Monster.CHARACTER_TYPE:
                difficulty = char.get_monster_ai_difficulty()
                if difficulty == "easy":
                    total_monster_difficulty_value += 1
                elif difficulty == "normal":
                    total_monster_difficulty_value += 2
                elif difficulty == "hard":
                    total_monster_difficulty_value += 3

        avg_player_level = (
            int(total_player_level / num_players) if num_players != 0 else 0
        )

        avg_monster_ai_difficulty_score = (
            total_monster_difficulty_value / num_monsters if num_monsters != 0 else 0
        )

        avg_monster_ai_difficulty_str: str
        if avg_monster_ai_difficulty_score == 0:
            avg_monster_ai_difficulty_str = "not available"
        elif round(avg_monster_ai_difficulty_score) == 1:
            avg_monster_ai_difficulty_str = "easy"
        elif round(avg_monster_ai_difficulty_score) == 2:
            avg_monster_ai_difficulty_str = "normal"
        else:
            avg_monster_ai_difficulty_str = "hard"

        return ServerStats(
            total_num_characters,
            num_monsters,
            num_players,
            avg_player_level,
            avg_monster_ai_difficulty_str,
        )

    def get_character_details(self, char_id: int) -> str:
        """Returns full details for a single character by ID."""

        self._validate_integer_id(self.ID_LABEL, char_id)
        character = self.get(char_id)
        return character.get_full_details()

    def get_character_details_by_type(self, character_type: str) -> list[str]:
        """Returns a list of brief details for characters of a specific type."""

        characters = self.get_all_by_type(character_type)
        return [char.get_details() for char in characters]

    def get_all_character_details(self) -> list[str]:
        """Returns a list of brief details for all characters on the server."""

        characters = self.get_all()
        return [char.get_details() for char in characters]
