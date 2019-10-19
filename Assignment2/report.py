from monster import Monster
from player import Player
from character_manager import CharacterManager
from abstract_character import AbstractCharacter


def main():
    acit = CharacterManager("ACIT")
    acit.add_character(1)
    print(acit.get_all())


if __name__ == "__main__":
    main()
