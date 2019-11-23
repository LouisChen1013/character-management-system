from abstract_character import AbstractCharacter
from sqlalchemy import Column, String, Integer, Float


class Monster(AbstractCharacter):
    """Represent a Monster class"""

    monster_ai_difficulty = Column(String(100))
    monster_type = Column(String(100))

    MONSTER_TYPE = ["dragon", "orc", "elf"]
    MONSTER_AI_DIFFICULTY = ["easy", "normal", "hard"]
    MONSTER_TYPE_LABEL = "Monster type"
    MONSTER_AI_DIFFICULTY_LABEL = "Monster AI difficulty"
    CHARACTER_TYPE = "monster"

    def __init__(self, monster_type, monster_ai_difficulty):
        """ Constructor - Initialize main attribute of Monster"""

        super().__init__(Monster.CHARACTER_TYPE)

        AbstractCharacter._validate_string_input(
            Monster.MONSTER_TYPE_LABEL, monster_type)
        if monster_type.lower() not in Monster.MONSTER_TYPE:
            raise ValueError("Monster type must be either dragon, orc or elf")

        AbstractCharacter._validate_string_input(
            Monster.MONSTER_AI_DIFFICULTY_LABEL, monster_ai_difficulty)
        if monster_ai_difficulty.lower() not in Monster.MONSTER_AI_DIFFICULTY:
            raise ValueError(
                "Monster AI difficulty must be either easy, normal, or hard")

        self.monster_ai_difficulty = monster_ai_difficulty.lower()
        self.monster_type = monster_type.lower()
        self.set_monster_type(self.monster_type)

    def set_monster_type(self, monster_type):
        """Set the monster type"""

        AbstractCharacter._validate_string_input(
            Monster.MONSTER_TYPE_LABEL, monster_type)
        if monster_type.lower() not in Monster.MONSTER_TYPE:
            raise ValueError("Monster type must be either dragon, orc, or elf")

        self.monster_type = monster_type.lower()

        if self.monster_type == "dragon":
            self.health = 150
        elif self.monster_type == "orc":
            self.health = 130
        elif self.monster_type == "elf":
            self.health = 110

    def get_monster_type(self):
        """Return the monster type"""

        return self.monster_type

    def set_monster_ai_difficulty(self, monster_ai_difficulty):
        """Set the monster AI difficulty"""

        AbstractCharacter._validate_string_input(
            Monster.MONSTER_AI_DIFFICULTY_LABEL, monster_ai_difficulty)
        if monster_ai_difficulty.lower() not in Monster.MONSTER_AI_DIFFICULTY:
            raise ValueError(
                "Monster AI difficulty must be either easy, normal, or hard")

        self.monster_ai_difficulty = monster_ai_difficulty.lower()

        if self.monster_ai_difficulty == "easy":
            self.damage = 10
        elif self.monster_ai_difficulty == "normal":
            self.damage = 20
        elif self.monster_ai_difficulty == "hard":
            self.damage = 30

    def get_monster_ai_difficulty(self):
        """Return the monster AI difficulty"""

        return self.monster_ai_difficulty

    def get_details(self):
        """Returns the description of the monster """

        details = f"The monster (id: {self.id}) is {self.get_monster_ai_difficulty()} {self.get_monster_type()} with {self.health} health and {self.damage} damage, Position: X = {self.get_position()[0]} Y = {self.get_position()[1]}"
        return details

    def get_type(self):
        """Returns monster for character type, this method overrides the get_type() method from AbstractCharacter parent class """

        return Monster.CHARACTER_TYPE

    def to_dict(self):
        """ Returns a dictionary representation of monster """

        dict = {}
        dict['id'] = self.id
        dict['health'] = self.health
        dict['damage'] = self.damage
        dict['position'] = self.get_position()
        dict['alive'] = self.alive
        dict['monster_ai_difficulty'] = self.monster_ai_difficulty
        dict['monster_type'] = self.monster_type
        dict['type'] = self.get_type()

        return dict
