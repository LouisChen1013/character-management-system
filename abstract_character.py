import re
from sqlalchemy import Column, String, Integer, Float
from base import Base


class AbstractCharacter(Base):
    """ Represent an abstract character """

    BOOLEAN_TRUE = 1

    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    health = Column(Integer)
    damage = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    alive = Column(Integer)
    type = Column(String(7))

    ID_LABEL = "ID"
    MIN_RANGE = 0
    MAX_RANGE = 10
    X_LABEL = "X"
    Y_LABEL = "Y"
    ALIVE_LABEL = "Alive"
    DAMAGE_LABEL = "Damage"
    HEALTH_LABEL = "Health"

    def __init__(self, type):
        """ Constructor - Initialize main attribute of AbstractCharacter"""
        
        AbstractCharacter._validate_string_input(
            AbstractCharacter.ID_LABEL, type)
        self.id = None
        self.health = 100
        self.damage = 10
        self.x = 0
        self.y = 0
        self.alive = True
        self.type = type

    def move_position(self, x, y):
        """ Moves position of character from x/y input """

        AbstractCharacter._validate_string_input(AbstractCharacter.X_LABEL, x)
        AbstractCharacter._validate_position(AbstractCharacter.X_LABEL, x)
        AbstractCharacter._validate_string_input(AbstractCharacter.Y_LABEL, y)
        AbstractCharacter._validate_position(AbstractCharacter.Y_LABEL, y)
        self.x = x
        self.y = y

    def get_position(self):
        """ Returns character position """
        position = [self.x, self.y]
        return position

    def set_alive(self, alive):
        """ Set characters existence status """

        AbstractCharacter._validate_string_input(
            AbstractCharacter.ALIVE_LABEL, alive)
        if alive is not isinstance(alive, bool):
            raise ValueError("Alive must be a Boolean (True/False)")
        self.alive = alive

    def get_alive(self):
        """ Returns characters existence Status """

        return self.alive

    def set_stats(self, damage, health):
        """ Sets characters status """

        AbstractCharacter._validate_string_input(
            AbstractCharacter.DAMAGE_LABEL, damage)
        if damage is not isinstance(damage, int):
            raise ValueError("Damage must an int")
        AbstractCharacter._validate_string_input(
            AbstractCharacter.HEALTH_LABEL, health)
        if health is not isinstance(health, int):
            raise ValueError("Health must an int")
        self.damage = damage
        self.health = health

    def get_stats(self):
        """ Returns characters stats """

        stats = []
        stats.append(self.damage)
        stats.append(self.health)
        return stats

    def get_type(self):
        """ Returns character type """

        # Abstract parent method
        raise NotImplementedError("Must implement in child class")

    def get_details(self):
        """ Returns character details """

        # Abstract parent method
        raise NotImplementedError("Must implement in child class")

    def get_full_details(self):
        """ Returns full character details """
        # Abstract parent method
        raise NotImplementedError("Must implement in child class")

    def to_dict(self):
        """ Adds the character to dict """

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
