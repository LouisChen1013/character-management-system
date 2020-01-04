from abstract_character import AbstractCharacter
from sqlalchemy import Column, String, Integer, Float


class Player(AbstractCharacter):
    """Represent a Player class"""

    player_level = Column(Integer)
    job = Column(String(100))

    PLAYER_JOB = ["assassin", "knight", "warrior"]
    LEVEL_RANGE = range(1, 11)
    PLAYER_LEVEL_LABEL = "Player Level"
    JOB_LABEL = "Player Job"
    CHARACTER_TYPE = "player"

    def __init__(self, player_level, job):
        """ Constructor - Initialize main attribute of Player"""

        super().__init__(Player.CHARACTER_TYPE)

        AbstractCharacter._validate_string_input(
            Player.PLAYER_LEVEL_LABEL, player_level)
        Player._validate_level(Player.PLAYER_LEVEL_LABEL, player_level)

        AbstractCharacter._validate_string_input(Player.JOB_LABEL, job)
        if job.lower() not in Player.PLAYER_JOB:
            raise ValueError(
                "Player Job must be either assassin, knight, or warrior")

        self.player_level = player_level
        self.job = job.lower()
        self.set_job(self.job)

    def set_level(self, player_level):
        """ Set Player Level """

        AbstractCharacter._validate_string_input(
            Player.PLAYER_LEVEL_LABEL, player_level)
        Player._validate_level(Player.PLAYER_LEVEL_LABEL, player_level)

        self.player_level = player_level

        if self.job == "assassin":
            self.health = 80 + ((self.player_level - 1) * 4)
            self.damage = 30 + ((self.player_level - 1) * 3)
        elif self.job == "knight":
            self.health = 100 + ((self.player_level - 1) * 4)
            self.damage = 20 + ((self.player_level - 1) * 3)
        elif self.job == "warrior":
            self.health = 120 + ((self.player_level - 1) * 4)
            self.damage = 10 + ((self.player_level - 1) * 3)

    def get_level(self):
        """ Returns Player Level """

        return self.player_level

    def set_job(self, job):
        """ Set Player Job """

        AbstractCharacter._validate_string_input(Player.JOB_LABEL, job)
        if job.lower() not in Player.PLAYER_JOB:
            raise ValueError(
                "Player Job must be either assassin, knight, or warrior")

        self.job = job.lower()

        if self.job == "assassin":
            self.health = 80 + ((self.player_level - 1) * 4)
            self.damage = 30 + ((self.player_level - 1) * 3)
        elif self.job == "knight":
            self.health = 100 + ((self.player_level - 1) * 4)
            self.damage = 20 + ((self.player_level - 1) * 3)
        elif self.job == "warrior":
            self.health = 120 + ((self.player_level - 1) * 4)
            self.damage = 10 + ((self.player_level - 1) * 3)

    def get_job(self):
        """ Return Player Job """

        return self.job

    def get_details(self):
        """Returns the description of the player"""

        details = f"The player (id: {self.id} ) is level {self.get_level()} {self.get_job()}"
        return details

    def get_full_details(self):

        full_details = f"The player (id: {self.id} ) is level {self.get_level()} {self.get_job()} with {self.health} health and {self.damage} damage, Position: X = {self.get_position()[0]} Y = {self.get_position()[1]}"
        return full_details

    def get_type(self):
        """Returns player for character type, this method overrides the get_type() method from AbstractCharacter parent class"""

        return Player.CHARACTER_TYPE

    def to_dict(self):
        """ Returns a dictionary representation of player """

        dict = {}
        dict['id'] = self.id
        dict['health'] = self.health
        dict['damage'] = self.damage
        dict['position'] = self.get_position()
        dict['alive'] = self.alive
        dict['player_level'] = self.player_level
        dict['job'] = self.job
        dict['type'] = self.get_type()

        return dict

    @staticmethod
    def _validate_level(display_value, level):
        """ Private helper to validate player level values """

        if level not in Player.LEVEL_RANGE:
            raise ValueError(
                display_value + " is out of range, please enter 1-10")
