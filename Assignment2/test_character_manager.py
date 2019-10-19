import unittest
import inspect
from monster import Monster
from player import Player
from character_manager import CharacterManager
from abstract_character import AbstractCharacter


class TestCharacterManager(unittest.TestCase):
    """ Unit test for Character Manager """

    def setUp(self):
        """ Initalizes test fixtures """
        self.logCharManager()
        self.server = CharacterManager("ACIT")
        self.player = Player(1, "assassin")
        self.monster = Monster("dragon", "easy")

    def test_server_valid_parameters(self):
        """ 010A - Valid Construction """
        self.assertIsNotNone(self.server, "Server name must be defined")

    def test_server_invalid_parameters(self):
        """ 010B - Invalid Construction Parameters """

        # Must reject an undefined server name
        undefined_server = None
        self.assertRaisesRegex(
            ValueError, "Server Name cannot be undefined", CharacterManager, undefined_server)

        # Must reject an empty server name
        empty_server = ""
        self.assertRaisesRegex(
            ValueError, "Server Name cannot be empty.", CharacterManager, empty_server)

        server_name = 1111
        self.assertNotEqual(
            ValueError, self.server.get_server_name(), server_name)

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
        self.assertEqual(len(self.server.get_all()), 1,
                         "Character list must still have 1 character")
        self.assertEqual(self.server.get_all()[0].get_id(
        ), 1, "ID of first character must still be 1")

        self.server.add_character(self.monster)
        self.assertEqual(len(self.server.get_all()), 2,
                         "Character list must still have 2 characters")
        self.assertEqual(self.server.get_all()[1].get_id(
        ), 2, "ID of first character must still be 2")

    def test_add_character_invalid(self):
        """ 020A - Valid Add Character """

        self.assertRaisesRegex(
            ValueError, "Character Object cannot be undefined", self.server.add_character, None)

        self.assertRaisesRegex(
            ValueError, "Character Object cannot be empty", self.server.add_character, "")

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

    def test_get(self):
        """ 040A - Get valid ID """
        self.server.add_character(self.monster)
        self.assertEqual(self.server.get(1).get_id(), 1)

    def test_get_all(self):
        """ 050A - Get a valid list of all characters """
        test_server = self.server.get_all()
        self.assertEqual(
            test_server, [], "Must return empty list if character list is empty")

    def test_get_all_by_type(self):
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
        self.server.add_character(self.monster)
        self.server.add_character(self.player)

        player = Player(1, "knight")
        player.set_id(1)
        self.server.update_character(player)
        self.assertEqual(self.server.get(1).get_type(), "player")

    def test_update_character_invalid(self):
        """ 070B - Invalid update character """
        self.assertRaisesRegex(
            ValueError, "Character Object cannot be undefined", self.server.update_character, None)

        self.assertRaisesRegex(
            ValueError, "Character Object cannot be empty", self.server.update_character, "")

    def test_delete_character(self):
        """ 080A - Validate successful removal of an existing character """
        self.server.delete_character(1)
        self.assertEqual(len(self.server.get_all()), 0,
                         "Character list must still have 0 characters")

        self.server.add_character(self.monster)
        self.server.delete_character(1)
        self.assertEqual(len(self.server.get_all()), 0,
                         "Character list must still have 0 characters")

        self.server.add_character(self.monster)
        self.server.add_character(self.player)
        self.server.delete_character(2)
        self.server.delete_character(1)
        self.assertEqual(len(self.server.get_all()), 1,
                         "Character list must still have 1 character")

    def test_delete_character_invalid(self):
        """ 080B - Validate unsuccessful removal of an existing character """
        self.assertRaisesRegex(
            ValueError, "ID cannot be undefined", self.server.delete_character, None)

        self.assertRaisesRegex(
            ValueError, "ID cannot be empty", self.server.delete_character, "")

        self.assertRaisesRegex(
            ValueError, "ID needs to be integer", self.server.delete_character, "123")

    def test_get_server_name(self):
        """ 090A - Get a valid Server Name """
        self.assertEqual(self.server.get_server_name(), "ACIT")

        self.assertNotEqual(self.server.get_server_name(), "BCIT")

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
