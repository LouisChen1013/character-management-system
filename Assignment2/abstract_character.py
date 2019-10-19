import re


class AbstractCharacter:
    # Represent an abstract character
    ID_LABEL = "ID"
    MIN_RANGE = 0
    MAX_RANGE = 10
    X_LABEL = "X"
    Y_LABEL = "Y"
    ALIVE_LABEL = "Alive"
    DAMAGE_LABEL = "Damage"
    HEALTH_LABEL = "Health"

    def __init__(self):

        AbstractCharacter._validate_string_input(
            AbstractCharacter.ID_LABEL, id)
        self._id = None
        self._health = 100
        self._damage = 10
        self._position = [0, 0]
        self._alive = True

    def move_position(self, x, y):
        AbstractCharacter._validate_string_input(AbstractCharacter.X_LABEL, x)
        AbstractCharacter._validate_position(AbstractCharacter.X_LABEL, x)
        AbstractCharacter._validate_string_input(AbstractCharacter.Y_LABEL, y)
        AbstractCharacter._validate_position(AbstractCharacter.Y_LABEL, y)
        self._position[0] = x
        self._position[1] = y

    def get_position(self):
        return self._position

    def set_alive(self, alive):
        AbstractCharacter._validate_string_input(
            AbstractCharacter.ALIVE_LABEL, alive)
        if alive is not isinstance(alive, bool):
            raise ValueError("Alive must be a Boolean (True/False)")
        self._alive = alive

    def get_alive(self):
        return self._alive

    def set_stats(self, damage, health):
        AbstractCharacter._validate_string_input(
            AbstractCharacter.DAMAGE_LABEL, damage)
        if damage is not isinstance(damage, int):
            raise ValueError("Damage must an int")
        AbstractCharacter._validate_string_input(
            AbstractCharacter.HEALTH_LABEL, health)
        if health is not isinstance(health, int):
            raise ValueError("Health must an int")
        self._damage = damage
        self._health = health

    def get_stats(self):
        stats = []
        stats.append(self._damage)
        stats.append(self._health)
        return stats

    def set_id(self, id):
        AbstractCharacter._validate_string_input(
            AbstractCharacter.ID_LABEL, id)
        self._id = id

    def get_id(self):
        return self._id

    def get_type(self):
        # Abstract parent method
        raise NotImplementedError("Must implement in child class")

    def get_details(self):
        # Abstract parent method
        raise NotImplementedError("Must implement in child class")

    @staticmethod
    def _validate_string_input(display_name, str_value):
        """ Private helper to validate string values """

        if str_value is None:
            raise ValueError(display_name + " cannot be undefined.")

        if str_value == "":
            raise ValueError(display_name + " cannot be empty.")

    @staticmethod
    def _validate_position(display_value, position_value):
        """ Private helper to validate position(x,y) values """

        if position_value < AbstractCharacter.MIN_RANGE or position_value > AbstractCharacter.MAX_RANGE:
            raise ValueError(display_value + " is out of range.")

        if position_value is not isinstance(position_value, int):
            raise ValueError(display_value + " must be an integer")
