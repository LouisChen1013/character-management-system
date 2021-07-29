import os, sys
p = os.path.abspath('.')
sys.path.insert(1, p)

import unittest
import inspect
from monster import Monster
from player import Player
from character_manager import CharacterManager
from abstract_character import AbstractCharacter
from sqlalchemy import create_engine
from base import Base
import os


class TestCharacterManager(unittest.TestCase):
    """ Unit test for Character Manager """

    def setUp(self):
        """ Initalizes test fixtures """

        engine = create_engine('sqlite:///test_characters.sqlite')

        # Creates all the tables
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine

        self.logCharManager()
        self.server = CharacterManager(
            "ACIT", "test_characters.sqlite")
        self.player = Player(1, "assassin")
        self.monster = Monster("dragon", "easy")

    def test_server_valid_parameters(self):
        """ 010A - Valid Construction """

        self.assertEqual(self.server._server_name, "ACIT",
                         "Server name must be ACIT")
        self.assertEqual(self.server._db_filename, "test_characters.sqlite")

    def test_server_invalid_parameters(self):
        """ 010B - Invalid Construction Parameters """

        # Must reject undefined server name
        self.assertRaisesRegex(
            ValueError, "Server Name cannot be undefined", CharacterManager, None, "test_characters.sqlite")

        # Must reject empty server name
        self.assertRaisesRegex(
            ValueError, "Server Name cannot be empty", CharacterManager, "", "test_characters.sqlite")

        # Must reject undefined filepath
        self.assertRaisesRegex(
            ValueError, "Database Name cannot be undefined", CharacterManager, "ACIT", None)

        # Must reject empty filepath
        self.assertRaisesRegex(
            ValueError, "Database Name cannot be empty", CharacterManager, "ACIT", "")

        # Must reject non-string server name
        self.assertRaisesRegex(
            ValueError, "Server Name must be string", CharacterManager, 1111, "test_characters.sqlite")

        # Must reject non-string filepath
        self.assertRaisesRegex(
            ValueError, "Database Name must be string", CharacterManager, "ACIT", 1111)

    def test_add_character_valid(self):
        """ 020A - Valid Add Character """
        self.assertEqual(len(self.server.get_all()), 0,
                         "Character list must have no characters")
        self.server.add_character(self.player)
        self.assertEqual(len(self.server.get_all()), 1,
                         "Character list must have 1 character")
        self.assertTrue(self.server.character_exists(self.server.get(1).id))

        player = Player(1, "knight")
        self.server.add_character(player)
        self.assertEqual(len(self.server.get_all()), 2,
                         "Character list must still have 2 character")
        self.assertTrue(self.server.character_exists(self.server.get(2).id))
        self.assertTrue(self.server.character_exists(self.server.get(1).id))

        self.server.add_character(self.monster)
        self.assertEqual(len(self.server.get_all()), 3,
                         "Character list must still have 3 characters")
        self.assertTrue(self.server.character_exists(self.server.get(3).id))

    def test_add_character_invalid(self):
        """ 020B - Invalid Add Character """

        self.assertRaisesRegex(
            ValueError, "Character Object cannot be undefined", self.server.add_character, None)

        self.assertRaisesRegex(
            ValueError, "Character Object cannot be empty", self.server.add_character, "")

        self.assertRaisesRegex(
            ValueError, "Invalid Character Object", self.server.add_character, "String Object")

    def test_character_exists_valid(self):
        """ 030A - Valid character exists in the list """

        self.assertFalse(self.server.character_exists(0),
                         "Character must not be in list")
        self.server.add_character(self.player)
        self.assertTrue(self.server.character_exists(1),
                        "Character must be in the list")
        self.server.add_character(self.player)
        self.assertTrue(self.server.character_exists(1),
                        "Character must be in the list")
        self.server.add_character(self.monster)
        self.assertTrue(self.server.character_exists(2),
                        "Character must be in the list")

    def test_character_exists_invalid(self):
        """ 030B - Invalid character exists in the list """

        self.assertRaisesRegex(
            ValueError, "ID cannot be undefined", self.server.character_exists, None)

        self.assertRaisesRegex(
            ValueError, "ID cannot be empty", self.server.character_exists, "")

        self.assertRaisesRegex(
            ValueError, "ID needs to be integer", self.server.character_exists, "123")

    def test_get_valid(self):
        """ 040A - Get valid ID """

        self.server.add_character(self.monster)
        self.assertTrue(self.server.character_exists(self.server.get(1).id))

    def test_get_invalid(self):
        """ 040B - Get invalid ID """

        self.assertRaisesRegex(
            ValueError, "ID cannot be undefined", self.server.get, None)

        self.assertRaisesRegex(
            ValueError, "ID cannot be empty", self.server.get, "")

        self.assertRaisesRegex(
            ValueError, "ID needs to be integer", self.server.get, "123")

    def test_get_all_valid(self):
        """ 050A - Get a valid list of all characters """

        test_server = self.server.get_all()
        self.assertEqual(
            test_server, [], "Must return empty list if character list is empty")

    def test_get_all_by_type_valid(self):
        """ 060A - Get a valid list of all characters based by type """

        self.assertEqual(len(self.server.get_all_by_type("player")), 0)
        self.assertEqual(len(self.server.get_all_by_type("monster")), 0)

        self.server.add_character(self.monster)
        self.server.add_character(self.player)
        player = Player(1, "knight")
        self.server.add_character(player)

        self.assertEqual(len(self.server.get_all_by_type("player")), 2)
        self.assertEqual(len(self.server.get_all_by_type("monster")), 1)

    def test_update_character_valid(self):
        """ 070A - Validate successful update of an existing character """

        self.server.add_character(self.player)
        self.server.add_character(self.monster)

        self.server.update_character(self.server.get(1).id, "knight", 5)
        self.server.update_character(self.server.get(2).id, "orc", "normal")
        self.assertEqual(self.server.get(1).get_job(), "knight")
        self.assertEqual(self.server.get(1).get_level(), 5)
        self.assertEqual(self.server.get(
            2).get_monster_ai_difficulty(), "normal")
        self.assertEqual(self.server.get(2).get_monster_type(), "orc")

    def test_update_character_invalid(self):
        """ 070B - Invalid update character """

        # check for job_type,level_difficulty input

        self.server.add_character(self.player)
        self.server.add_character(self.monster)

        self.assertRaisesRegex(
            ValueError, "ID cannot be undefined", self.server.update_character, None, "knight", 1)

        self.assertRaisesRegex(
            ValueError, "ID cannot be empty", self.server.update_character, "", "knight", 1)

        self.assertRaisesRegex(
            ValueError, "ID needs to be integer", self.server.update_character, "123", "knight", 1)

        self.assertRaisesRegex(
            ValueError, "Job/Type cannot be undefined", self.server.update_character, 1, None, 1)

        self.assertRaisesRegex(
            ValueError, "Job/Type cannot be empty", self.server.update_character, 1, "", 1)

        self.assertRaisesRegex(
            ValueError, "Level needs to be integer", self.server.update_character, 1, "knight", "1")

        self.assertRaisesRegex(
            ValueError, "Difficulty cannot be empty", self.server.update_character, 2, "orc", "")

        self.assertRaisesRegex(
            ValueError, "Difficulty cannot be undefined", self.server.update_character, 2, "orc", None)

    def test_delete_character_valid(self):
        """ 080A - Validate successful removal of an existing character """

        self.server.add_character(self.monster)
        self.server.delete_character(1)
        monster = Monster("orc", "easy")
        self.server.add_character(monster)
        self.server.add_character(self.player)
        self.server.delete_character(1)
        self.server.delete_character(2)
        self.assertEqual(len(self.server.get_all()), 0,
                         "Character list must still have 0 characters")

    def test_delete_character_invalid(self):
        """ 080B - Validate unsuccessful removal of an existing character """

        self.assertRaisesRegex(
            ValueError, "ID cannot be undefined", self.server.delete_character, None)

        self.assertRaisesRegex(
            ValueError, "ID cannot be empty", self.server.delete_character, "")

        self.assertRaisesRegex(
            ValueError, "ID needs to be integer", self.server.delete_character, "123")

    def test_get_server_name_valid(self):
        """ 090A - Get a valid Server Name """

        self.assertEqual(self.server.get_server_name(), "ACIT")

        self.assertNotEqual(self.server.get_server_name(), "BCIT")

    def test_get_server_stats_valid(self):
        """ 100A - Get valid server stats """

        # No stats
        server1 = self.server.get_server_stats()
        self.assertEqual(0, server1.get_total_num_characters())
        self.assertEqual(0, server1.get_num_monsters())
        self.assertEqual(0, server1.get_num_players())
        self.assertEqual(0, server1.get_avg_player_level())
        self.assertEqual(
            "not available", server1.get_avg_monster_ai_difficulty())

        # Some stats
        self.server.add_character(self.monster)
        self.server.add_character(self.player)

        server2 = self.server.get_server_stats()
        self.assertEqual(2, server2.get_total_num_characters())
        self.assertEqual(1, server2.get_num_monsters())
        self.assertEqual(1, server2.get_num_players())
        self.assertEqual(1, server2.get_avg_player_level())
        self.assertEqual(
            "easy", server2.get_avg_monster_ai_difficulty())

    def test_get_character_details_by_type_valid(self):
        """ 110A - Get valid character details by type  """

        # No Player and Monster Character
        details1 = self.server.get_character_details_by_type(
            Player.CHARACTER_TYPE)
        self.assertEqual(0, len(details1))

        details2 = self.server.get_character_details_by_type(
            Monster.CHARACTER_TYPE)
        self.assertEqual(0, len(details2))

        # Some Player and Monster Character
        self.server.add_character(self.monster)
        self.server.add_character(self.player)

        details3 = self.server.get_character_details_by_type(
            Player.CHARACTER_TYPE)
        self.assertEqual(1, len(details3))

        details4 = self.server.get_character_details_by_type(
            Monster.CHARACTER_TYPE)
        self.assertEqual(1, len(details4))

    def test_get_character_details_by_type_invalid(self):
        """ 110B - Invalid character details by type  """

        self.assertRaisesRegex(ValueError, "Invalid character type",
                               self.server.get_character_details_by_type, None)
        self.assertRaisesRegex(ValueError, "Invalid character type",
                               self.server.get_character_details_by_type, "Random")

    def test_get_all_character_details_valid(self):
        """ 120A - Get all valid character details """

        # No Player and Monster Character
        details1 = self.server.get_all_character_details()
        self.assertEqual(0, len(details1))

        # Some Player and Monster Character

        self.server.add_character(self.monster)
        self.server.add_character(self.player)

        details2 = self.server.get_all_character_details()
        self.assertEqual(2, len(details2))

    def test_get_character_details_valid(self):
        """ 130A - Get a valid character details """

        # Details for Player and Monster Character
        self.server.add_character(self.monster)
        self.server.add_character(self.player)

        details1 = self.server.get_character_details(1)
        self.assertEqual(
            "The monster (id: 1 ) is easy dragon with 150 health and 10 damage, Position: X = 0 Y = 0", details1)
        details2 = self.server.get_character_details(2)
        self.assertEqual(
            "The player (id: 2 ) is level 1 assassin with 80 health and 30 damage, Position: X = 0 Y = 0", details2)

    def test_get_character_details_invalid(self):
        """ 130B - Get invalid character details """

        self.assertRaisesRegex(
            ValueError, "ID cannot be undefined", self.server.get_character_details, None)

        self.assertRaisesRegex(
            ValueError, "ID cannot be empty", self.server.get_character_details, "")

        self.assertRaisesRegex(
            ValueError, "ID needs to be integer", self.server.get_character_details, "123")

    def tearDown(self):
        """" Tear down """
        os.remove("test_characters.sqlite")
        self.logCharManager()

    def logCharManager(self):
        """ Logs Character Manager """

        currentTest = self.id().split('.')[-1]
        callingFunction = inspect.stack()[1][3]
        print('in %s - %s()' % (currentTest, callingFunction))


if __name__ == "__main__":
    unittest.main()
