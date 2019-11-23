import unittest
import inspect
from monster import Monster
from player import Player
from character_manager import CharacterManager
from abstract_character import AbstractCharacter
from unittest.mock import patch, mock_open


class TestCharacterManager(unittest.TestCase):
    """ Unit test for Character Manager """

    @patch('builtins.open', mock_open(read_data='[]'))
    def setUp(self):
        """ Initalizes test fixtures """

        self.logCharManager()
        self.server = CharacterManager(
            "ACIT", "/Users/QB/Desktop/Pure_Python/Assignment2")
        self.player = Player(1, "assassin")
        self.monster = Monster("dragon", "easy")

    @patch('builtins.open', mock_open(read_data='[]'))
    def test_server_valid_parameters(self):
        """ 010A - Valid Construction """

        self.assertEqual(self.server._server_name, "ACIT",
                         "Server name must be ACIT")
        self.assertEqual(self.server._filepath,
                         "/Users/QB/Desktop/Pure_Python/Assignment2")

    @patch('builtins.open', mock_open(read_data='[]'))
    def test_server_invalid_parameters(self):
        """ 010B - Invalid Construction Parameters """

        # Must reject undefined server name
        self.assertRaisesRegex(
            ValueError, "Server Name cannot be undefined", CharacterManager, None, "/Users/QB/Desktop/Pure_Python/Assignment2")

        # Must reject empty server name
        self.assertRaisesRegex(
            ValueError, "Server Name cannot be empty", CharacterManager, "", "/Users/QB/Desktop/Pure_Python/Assignment2")

        # Must reject undefined filepath
        self.assertRaisesRegex(
            ValueError, "Filepath cannot be undefined", CharacterManager, "ACIT", None)

        # Must reject empty filepath
        self.assertRaisesRegex(
            ValueError, "Filepath cannot be empty", CharacterManager, "ACIT", "")

        # Must reject non-string server name
        self.assertRaisesRegex(
            ValueError, "Server Name must be string", CharacterManager, 1111, "/Users/QB/Desktop/Pure_Python/Assignment2")

        # Must reject non-string filepath
        self.assertRaisesRegex(
            ValueError, "Filepath must be string", CharacterManager, "ACIT", 1111)

    @patch('builtins.open', mock_open(read_data='[]'))
    def test_add_character_valid(self):
        """ 020A - Valid Add Character """

        self.assertEqual(len(self.server.get_all()), 0,
                         "Character list must have no characters")

        self.server.add_character(self.player)
        self.assertEqual(len(self.server.get_all()), 1,
                         "Character list must have 1 character")

        self.assertEqual(self.server.get_all()[
                         0].get_id(), 1, "ID of first character must be 1")

        player = Player(1, "knight")
        player.set_id(1)

        self.server.add_character(player)
        self.assertEqual(len(self.server.get_all()), 2,
                         "Character list must still have 2 character")
        self.assertEqual(self.server.get_all()[0].get_id(
        ), 1, "ID of first character must still be 1")

        self.server.add_character(self.monster)
        self.assertEqual(len(self.server.get_all()), 3,
                         "Character list must still have 3 characters")
        self.assertEqual(self.server.get_all()[1].get_id(
        ), 2, "ID of first character must still be 2")

    @patch('builtins.open', mock_open(read_data='[]'))
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
        self.assertEqual(self.server.get(1).get_id(), 1)

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

    @patch('builtins.open', mock_open(read_data='[]'))
    def test_update_character_valid(self):
        """ 070A - Validate successful update of an existing character """

        self.server.add_character(self.monster)
        self.server.add_character(self.player)

        player = Player(1, "knight")
        player.set_id(1)
        self.server.update_character(player)
        self.assertEqual(self.server.get(1).get_type(), "player")

    @patch('builtins.open', mock_open(read_data='[]'))
    def test_update_character_invalid(self):
        """ 070B - Invalid update character """

        self.assertRaisesRegex(
            ValueError, "Character Object cannot be undefined", self.server.update_character, None)

        self.assertRaisesRegex(
            ValueError, "Character Object cannot be empty", self.server.update_character, "")

        self.assertRaisesRegex(
            ValueError, "Invalid Character Object", self.server.add_character, "String Object")

    @patch('builtins.open', mock_open(read_data='[]'))
    def test_delete_character_valid(self):
        """ 080A - Validate successful removal of an existing character """

        self.server.add_character(self.monster)
        self.server.delete_character(1)
        self.assertEqual(len(self.server.get_all()), 0,
                         "Character list must still have 0 characters")

        self.server.add_character(self.monster)
        self.server.add_character(self.player)
        self.server.delete_character(2)
        self.server.delete_character(3)
        self.assertEqual(len(self.server.get_all()), 0,
                         "Character list must still have 0 characters")

    @patch('builtins.open', mock_open(read_data='[]'))
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

    def test_get_assigned_id_valid(self):
        """ 100A - Get valid assigned id """

        self.assertEqual(self.server.get_assigned_id(), 0)
        self.server.add_character(self.monster)
        self.assertEqual(self.server.get_assigned_id(), 1)
        self.server.add_character(self.player)
        self.assertEqual(self.server.get_assigned_id(), 2)

    def test_get_server_stats_valid(self):
        """ 110A - Get valid server stats """

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
        """ 120A - Get valid character details by type  """

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
        """ 120B - Invalid character details by type  """

        self.assertRaisesRegex(ValueError, "Invalid character type",
                               self.server.get_character_details_by_type, None)
        self.assertRaisesRegex(ValueError, "Invalid character type",
                               self.server.get_character_details_by_type, "Random")

    def test_get_all_character_details_valid(self):
        """ 130A - Get all valid character details """

        # No Player and Monster Character
        details1 = self.server.get_all_character_details()
        self.assertEqual(0, len(details1))

        # Some Player and Monster Character

        self.server.add_character(self.monster)
        self.server.add_character(self.player)

        details2 = self.server.get_all_character_details()
        self.assertEqual(2, len(details2))

    def tearDown(self):
        """" Tear down """

        self.logCharManager()

    def logCharManager(self):
        """ Logs Character Manager """

        currentTest = self.id().split('.')[-1]
        callingFunction = inspect.stack()[1][3]
        print('in %s - %s()' % (currentTest, callingFunction))


if __name__ == "__main__":
    unittest.main()
