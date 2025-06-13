from sqlalchemy import Column, String, Integer
from base import Base


class AbstractCharacter(Base):
    """Represent an abstract character"""

    __tablename__ = "characters"

    id: Column[Integer] = Column(Integer, primary_key=True)
    health: Column[Integer] = Column(Integer)
    damage: Column[Integer] = Column(Integer)
    x: Column[Integer] = Column(Integer)
    y: Column[Integer] = Column(Integer)
    alive: Column[Integer] = Column(Integer)
    type: Column[String] = Column(String(7))

    __mapper_args__ = {"polymorphic_on": type}

    ID_LABEL = "ID"
    MIN_RANGE = 0
    MAX_RANGE = 10
    X_LABEL = "X"
    Y_LABEL = "Y"
    ALIVE_LABEL = "Alive"
    DAMAGE_LABEL = "Damage"
    HEALTH_LABEL = "Health"

    def __init__(self, char_type: str):
        """Constructor - Initialize main attributes of AbstractCharacter."""
        self._validate_character_type_input(char_type)

        self.id = None
        self.health = 100
        self.damage = 10
        self.x = 0
        self.y = 0
        self.alive = True
        self.type = char_type

    def _validate_character_type_input(self, char_type_value):
        """Private helper to validate the character type string."""
        if not isinstance(char_type_value, str):
            raise ValueError(f"{self.ID_LABEL} (Character Type) must be a string.")
        AbstractCharacter._validate_string_input(self.ID_LABEL, char_type_value)

    def move_position(self, x: int, y: int):
        """Moves position of character to x/y input"""

        self._validate_position_input(self.X_LABEL, x)
        self._validate_position_input(self.Y_LABEL, y)
        self.x = x
        self.y = y

    def get_position(self) -> list[int]:
        """Returns character position as a list [x, y]"""
        return [self.x, self.y]

    def set_alive(self, alive_status: bool):
        """Set characters existence status"""

        if not isinstance(alive_status, bool):
            raise ValueError(f"{self.ALIVE_LABEL} must be a Boolean (True/False).")
        self.alive = alive_status

    def get_alive(self) -> bool:
        """Returns characters existence Status"""
        return self.alive

    def set_stats(self, damage: int, health: int):
        """Sets characters damage and health stats"""

        if not isinstance(damage, int):
            raise ValueError(f"{self.DAMAGE_LABEL} must be an integer.")
        if not isinstance(health, int):
            raise ValueError(f"{self.HEALTH_LABEL} must be an integer.")

        AbstractCharacter._validate_string_input(self.DAMAGE_LABEL, damage)
        AbstractCharacter._validate_string_input(self.HEALTH_LABEL, health)

        self.damage = damage
        self.health = health

    def get_stats(self) -> list[int]:
        """Returns characters stats as a list [damage, health]"""
        return [self.damage, self.health]

    def get_type(self) -> str:
        """Returns character type. Abstract method."""
        raise NotImplementedError("Must implement in child class")

    def get_details(self) -> str:
        """Returns character details. Abstract method."""
        raise NotImplementedError("Must implement in child class")

    def get_full_details(self) -> str:
        """Returns full character details. Abstract method."""
        raise NotImplementedError("Must implement in child class")

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the character. Abstract method."""
        raise NotImplementedError("Must implement in child class")

    @staticmethod
    def _validate_string_input(display_name: str, value):
        """
        Private helper to validate string values for being non-None and non-empty.
        It handles cases where 'value' might not be a string, letting specific
        type checks occur elsewhere if needed.
        """
        if value is None:
            raise ValueError(f"{display_name} cannot be undefined (None).")

        if isinstance(value, str) and value == "":
            raise ValueError(f"{display_name} cannot be empty.")

    @staticmethod
    def _validate_position_input(display_name: str, position_value: int):
        """Private helper to validate position (x,y) values for type and range."""
        if not isinstance(position_value, int):
            raise ValueError(f"{display_name} must be an integer.")

        if not (
            AbstractCharacter.MIN_RANGE <= position_value <= AbstractCharacter.MAX_RANGE
        ):
            raise ValueError(
                f"{display_name} ({position_value}) is out of range. Must be between {AbstractCharacter.MIN_RANGE} and {AbstractCharacter.MAX_RANGE}."
            )
