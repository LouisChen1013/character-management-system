from abstract_character import AbstractCharacter
from sqlalchemy import Column, String


class Monster(AbstractCharacter):
    """Represent a Monster class"""

    __mapper_args__ = {"polymorphic_identity": "monster"}

    monster_ai_difficulty = Column(String(100))
    monster_type = Column(String(100))

    MONSTER_TYPE = ["dragon", "orc", "elf"]
    MONSTER_AI_DIFFICULTY = ["easy", "normal", "hard"]
    MONSTER_TYPE_LABEL = "Monster type"
    MONSTER_AI_DIFFICULTY_LABEL = "Monster AI difficulty"
    CHARACTER_TYPE = "monster"

    def __init__(self, monster_type: str, monster_ai_difficulty: str):
        """Constructor - Initialize main attribute of Monster"""

        super().__init__(Monster.CHARACTER_TYPE)

        self._set_initial_monster_type(monster_type)
        self._set_initial_monster_ai_difficulty(monster_ai_difficulty)

        self._update_stats_based_on_type_and_difficulty()

    def _validate_input_string(self, label: str, value):
        """Helper to validate if an input is a non-empty string."""
        if not isinstance(value, str):
            raise ValueError(f"{label} must be a string.")
        AbstractCharacter._validate_string_input(label, value)

    def _set_initial_monster_type(self, monster_type_value: str):
        """Internal method for initial validation and setting of monster_type."""
        self._validate_input_string(Monster.MONSTER_TYPE_LABEL, monster_type_value)
        if monster_type_value.lower() not in Monster.MONSTER_TYPE:
            raise ValueError("Monster type must be either dragon, orc or elf")
        self.monster_type = monster_type_value.lower()

    def _set_initial_monster_ai_difficulty(self, monster_ai_difficulty_value: str):
        """Internal method for initial validation and setting of monster_ai_difficulty."""
        self._validate_input_string(
            Monster.MONSTER_AI_DIFFICULTY_LABEL, monster_ai_difficulty_value
        )
        if monster_ai_difficulty_value.lower() not in Monster.MONSTER_AI_DIFFICULTY:
            raise ValueError(
                "Monster AI difficulty must be either easy, normal, or hard."
            )
        self.monster_ai_difficulty = monster_ai_difficulty_value.lower()

    def set_monster_type(self, monster_type: str):
        """Set the monster type and recalculate all stats."""
        self._set_initial_monster_type(monster_type)
        self._update_stats_based_on_type_and_difficulty()

    def get_monster_type(self) -> str:
        """Return the monster type."""
        return self.monster_type

    def set_monster_ai_difficulty(self, monster_ai_difficulty: str):
        """Set the monster AI difficulty and recalculate all stats."""
        self._set_initial_monster_ai_difficulty(monster_ai_difficulty)
        self._update_stats_based_on_type_and_difficulty()

    def _update_stats_based_on_type_and_difficulty(self):
        """
        Helper to update health and damage based on the current
        monster_type and monster_ai_difficulty.
        """
        # Set base health based on type
        if self.monster_type == "dragon":
            self.health = 150
        elif self.monster_type == "orc":
            self.health = 130
        elif self.monster_type == "elf":
            self.health = 110
        else:
            self.health = 100

        # Set base damage based on AI difficulty
        if self.monster_ai_difficulty == "easy":
            self.damage = 10
        elif self.monster_ai_difficulty == "normal":
            self.damage = 20
        elif self.monster_ai_difficulty == "hard":
            self.damage = 30
        else:
            self.damage = 15

    def get_monster_ai_difficulty(self) -> str:
        """Return the monster AI difficulty."""
        return self.monster_ai_difficulty

    def get_details(self) -> str:
        """Returns a brief description of the monster."""
        return f"The monster (id: {self.id}) is {self.get_monster_ai_difficulty()} {self.get_monster_type()}"

    def get_full_details(self) -> str:
        """Returns the full description of the monster, including position and stats."""
        x, y = self.get_position()
        return (
            f"The monster (id: {self.id}) is {self.get_monster_ai_difficulty()} "
            f"{self.get_monster_type()} with {self.health} health and {self.damage} damage, "
            f"Position: X = {x} Y = {y}"
        )

    def get_type(self) -> str:
        """Returns 'monster' for character type, overriding the method from AbstractCharacter parent class."""
        return Monster.CHARACTER_TYPE

    def to_dict(self) -> dict:
        """Returns a dictionary representation of monster."""
        return {
            "id": self.id,
            "health": self.health,
            "damage": self.damage,
            "position": self.get_position(),
            "alive": self.alive,
            "monster_ai_difficulty": self.monster_ai_difficulty,
            "monster_type": self.monster_type,
            "type": self.get_type(),
        }
