from abstract_character import AbstractCharacter
from sqlalchemy import Column, String, Integer, Float


class Player(AbstractCharacter):
    """Represent a Player class"""

    PLAYER_JOB = ["assassin", "knight", "warrior"]
    LEVEL_RANGE = range(1, 11)
    PLAYER_LEVEL_LABEL = "Player Level"
    JOB_LABEL = "Player Job"
    CHARACTER_TYPE = "player"

    def __init__(self, player_level, job):
        """ Constructor - Initialize main attribute of Player"""

        super().__init__()

        AbstractCharacter._validate_string_input(
            Player.PLAYER_LEVEL_LABEL, player_level)
        Player._validate_level(Player.PLAYER_LEVEL_LABEL, player_level)

        AbstractCharacter._validate_string_input(Player.JOB_LABEL, job)
        if job.lower() not in Player.PLAYER_JOB:
            raise ValueError(
                "Player Job must be either assassin, knight, or warrior")

        self._player_level = player_level
        self._job = job.lower()
        self.set_job(self._job)

    def set_level(self, player_level):
        """ Set Player Level """

        AbstractCharacter._validate_string_input(
            Player.PLAYER_LEVEL_LABEL, player_level)
        Player._validate_level(Player.PLAYER_LEVEL_LABEL, player_level)

        self._player_level = player_level

        if self._job == "assassin":
            self._health = 80 + ((self._player_level - 1) * 4)
            self._damage = 30 + ((self._player_level - 1) * 3)
        elif self._job == "knight":
            self._health = 100 + ((self._player_level - 1) * 4)
            self._damage = 20 + ((self._player_level - 1) * 3)
        elif self._job == "warrior":
            self._health = 120 + ((self._player_level - 1) * 4)
            self._damage = 10 + ((self._player_level - 1) * 3)

    def get_level(self):
        """ Returns Player Level """

        return self._player_level

    def set_job(self, job):
        """ Set Player Job """

        AbstractCharacter._validate_string_input(Player.JOB_LABEL, job)
        if job.lower() not in Player.PLAYER_JOB:
            raise ValueError(
                "Player Job must be either assassin, knight, or warrior")

        self._job = job.lower()

        if self._job == "assassin":
            self._health = 80 + ((self._player_level - 1) * 4)
            self._damage = 30 + ((self._player_level - 1) * 3)
        elif self._job == "knight":
            self._health = 100 + ((self._player_level - 1) * 4)
            self._damage = 20 + ((self._player_level - 1) * 3)
        elif self._job == "warrior":
            self._health = 120 + ((self._player_level - 1) * 4)
            self._damage = 10 + ((self._player_level - 1) * 3)

    def get_job(self):
        """ Return Player Job """

        return self._job

    def get_details(self):
        """Returns the description of the player"""

        details = f"The player (id: {self.get_id()}) is level {self.get_level()} {self.get_job()} with {self._health} health and {self._damage} damage, Position: X = {self._position[0]} Y = {self._position[1]}"
        return details

    def get_type(self):
        """Returns player for character type, this method overrides the get_type() method from AbstractCharacter parent class"""
        
        return Player.CHARACTER_TYPE

    def to_dict(self):
        """ Returns a dictionary representation of player """

        dict = {}
        dict['id'] = self._id
        dict['health'] = self._health
        dict['damage'] = self._damage
        dict['position'] = self._position
        dict['alive'] = self._alive
        dict['player_level'] = self._player_level
        dict['job'] = self._job
        dict['type'] = self.get_type()

        return dict

    @staticmethod
    def _validate_level(display_value, level):
        """ Private helper to validate player level values """
        
        if level not in Player.LEVEL_RANGE:
            raise ValueError(
                display_value + " is out of range, please enter 0-10")
