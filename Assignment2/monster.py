from abstract_character import AbstractCharacter


class Monster(AbstractCharacter):
    """Represent a Monster class"""
    MONSTER_TYPE = ["dragon", "orc", "elf"]
    MONSTER_AI_DIFFICULTY = ["easy", "normal", "hard"]
    MONSTER_TYPE_LABEL = "Monster type"
    MONSTER_AI_DIFFICULTY_LABEL = "Monster AI difficulty"

    def __init__(self, monster_type, monster_ai_difficulty):
        """initializes a monster"""

        super().__init__()

        AbstractCharacter._validate_string_input(
            Monster.MONSTER_TYPE_LABEL, monster_type)
        if monster_type.lower() not in Monster.MONSTER_TYPE:
            raise ValueError("Monster type must be either dragon, orc or elf")

        AbstractCharacter._validate_string_input(
            Monster.MONSTER_AI_DIFFICULTY_LABEL, monster_ai_difficulty)
        if monster_ai_difficulty.lower() not in Monster.MONSTER_AI_DIFFICULTY:
            raise ValueError(
                "Monster AI difficulty must be either easy, normal, or hard")

        self._monster_ai_difficulty = monster_ai_difficulty.lower()
        self._monster_type = monster_type.lower()
        self.set_monster_type(self._monster_type)

    def set_monster_type(self, monster_type):
        """Set the monster type"""
        AbstractCharacter._validate_string_input(
            Monster.MONSTER_TYPE_LABEL, monster_type)
        if monster_type.lower() not in Monster.MONSTER_TYPE:
            raise ValueError("Monster type must be either dragon, orc, or elf")

        self._monster_type = monster_type.lower()

        if self._monster_type == "dragon":
            self._health = 150
        elif self._monster_type == "orc":
            self._health = 130
        elif self._monster_type == "elf":
            self._health = 110

    def get_monster_type(self):
        """Return the monster type"""
        return self._monster_type

    def set_monster_ai_difficulty(self, monster_ai_difficulty):
        """Set the monster AI difficulty"""
        AbstractCharacter._validate_string_input(
            Monster.MONSTER_AI_DIFFICULTY_LABEL, monster_ai_difficulty)
        if monster_ai_difficulty.lower() not in Monster.MONSTER_AI_DIFFICULTY:
            raise ValueError(
                "Monster AI difficulty must be either easy, normal, or hard")

        self._monster_ai_difficulty = monster_ai_difficulty.lower()

        if self._monster_ai_difficulty == "easy":
            self._damage = 10
        elif self._monster_ai_difficulty == "normal":
            self._damage = 20
        elif self._monster_ai_difficulty == "hard":
            self._damage = 30

    def get_monster_ai_difficulty(self):
        """Return the monster AI difficulty"""
        return self._monster_ai_difficulty

    def get_details(self):
        """Returns the description of the monster"""
        # details = "The monster(id) is {difficulty} {type}  and with {health} and {damage}, Position:{}".format()
        details = f"The monster is {self.get_monster_ai_difficulty()} {self.get_monster_type()} with {self._health} health and {self._damage} damage, Position: X = {self._position[0]} Y = {self._position[1]}"
        return details

    def get_type(self):
        """Returns monster for character type, this method overrides the get_type() method from AbstractMobileDeive parent class"""
        CHARACTER_TYPE = "monster"
        return CHARACTER_TYPE
