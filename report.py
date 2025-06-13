from monster import Monster
from player import Player
from character_manager import CharacterManager


def main():
    """TEST REPORT"""
    acit = CharacterManager("ACIT", "characters.sqlite")

    player1 = Player(1, "knight")
    player2 = Player(2, "assassin")
    monster1 = Monster("dragon", "hard")

    acit.add_character(player1)
    acit.add_character(player2)
    acit.add_character(monster1)

    # print(acit.get(1).to_dict())
    print([c.to_dict() for c in acit.get_all()])


if __name__ == "__main__":
    main()
