from abstract_character import AbstractCharacter
from sqlalchemy import Column, String, Integer


class Player(AbstractCharacter):
    """Represent a Player class"""

    __mapper_args__ = {"polymorphic_identity": "player"}

    player_level = Column(Integer)
    job = Column(String(100))

    PLAYER_JOB = ["assassin", "knight", "warrior"]
    LEVEL_RANGE = range(1, 11)
    PLAYER_LEVEL_LABEL = "Player Level"
    JOB_LABEL = "Player Job"
    CHARACTER_TYPE = "player"

    def __init__(self, player_level: int, job: str):
        """Constructor - Initialize main attribute of Player"""

        super().__init__(Player.CHARACTER_TYPE)

        self._set_initial_player_level(player_level)
        self._set_initial_job(job)

        self._update_stats_based_on_job_and_level()

    def _validate_player_level_input(self, level_value):
        """Private helper to validate player level input type and range."""
        if not isinstance(level_value, int):
            raise ValueError(f"{Player.PLAYER_LEVEL_LABEL} must be an integer.")
        if level_value not in Player.LEVEL_RANGE:
            raise ValueError(
                f"{Player.PLAYER_LEVEL_LABEL} is out of range, please enter 1-10"
            )

    def _set_initial_player_level(self, player_level_value: int):
        """Internal method for initial validation and setting of player_level."""
        AbstractCharacter._validate_string_input(
            Player.PLAYER_LEVEL_LABEL, player_level_value
        )
        self._validate_player_level_input(player_level_value)
        self.player_level = player_level_value

    def _validate_job_input(self, job_value):
        """Private helper to validate job input type and accepted values."""
        if not isinstance(job_value, str):
            raise ValueError(f"{Player.JOB_LABEL} must be a string.")
        AbstractCharacter._validate_string_input(Player.JOB_LABEL, job_value)
        if job_value.lower() not in Player.PLAYER_JOB:
            raise ValueError("Player Job must be either assassin, knight, or warrior.")

    def _set_initial_job(self, job_value: str):
        """Internal method for initial validation and setting of job."""
        self._validate_job_input(job_value)
        self.job = job_value.lower()

    def set_level(self, player_level: int):
        """Set Player Level and recalculate all stats."""

        self._set_initial_player_level(player_level)
        self._update_stats_based_on_job_and_level()

    def get_level(self) -> int:
        """Returns Player Level"""

        return self.player_level

    def set_job(self, job: str):
        """Set Player Job and recalculate all stats."""

        self._set_initial_job(job)
        self._update_stats_based_on_job_and_level()

    def _update_stats_based_on_job_and_level(self):
        """Helper to update health and damage based on current job and level."""
        if self.job == "assassin":
            self.health = 80 + ((self.player_level - 1) * 4)
            self.damage = 30 + ((self.player_level - 1) * 3)
        elif self.job == "knight":
            self.health = 100 + ((self.player_level - 1) * 4)
            self.damage = 20 + ((self.player_level - 1) * 3)
        elif self.job == "warrior":
            self.health = 120 + ((self.player_level - 1) * 4)
            self.damage = 10 + ((self.player_level - 1) * 3)
        else:
            self.health = 100
            self.damage = 10

    def get_job(self) -> str:
        """Return Player Job"""

        return self.job

    def get_details(self) -> str:
        """Returns the description of the player"""

        details = (
            f"The player (id: {self.id}) is level {self.get_level()} {self.get_job()}"
        )
        return details

    def get_full_details(self) -> str:
        """Returns full player details"""

        full_details = f"The player (id: {self.id}) is level {self.get_level()} {self.get_job()} with {self.health} health and {self.damage} damage, Position: X = {self.get_position()[0]} Y = {self.get_position()[1]}"
        return full_details

    def get_type(self) -> str:
        """Returns 'player' for character type, overriding the method from AbstractCharacter parent class."""

        return Player.CHARACTER_TYPE

    def to_dict(self) -> dict:
        """Returns a dictionary representation of player"""

        return {
            "id": self.id,
            "health": self.health,
            "damage": self.damage,
            "position": self.get_position(),
            "alive": self.alive,
            "player_level": self.player_level,
            "job": self.job,
            "type": self.get_type(),
        }

    @staticmethod
    def _validate_level(display_value, level):
        """Private helper to validate player level values."""
        if level not in Player.LEVEL_RANGE:
            raise ValueError(f"{display_value} is out of range, please enter 1-10")
