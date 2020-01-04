from monster import Monster
from player import Player
from character_manager import CharacterManager
from abstract_character import AbstractCharacter


def main():
    """ TEST REPORT """
    acit = CharacterManager(
        "ACIT", "characters")
    player1 = Player(1, "knight")
    player2 = Player(1, "knight")
    acit.add_character(player1)
    acit.add_character(player2)

    print(acit.get(1))

    print(acit.get_all())


if __name__ == "__main__":
    main()
