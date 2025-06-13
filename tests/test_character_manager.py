import os
import sys
from sqlalchemy import create_engine

# project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add project root to Python module search path if it's not already included
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import unittest
from monster import Monster
from player import Player
from character_manager import CharacterManager
from base import Base


class TestCharacterManager(unittest.TestCase):
    """Unit test for Character Manager"""

    DB_FILE = "test_characters.sqlite"

    def setUp(self):
        """Initialize fixtures"""
        # Ensure a clean database file for each test
        if os.path.exists(self.DB_FILE):
            os.remove(self.DB_FILE)

        # 1. Create a single Engine instance for this test
        self.engine = create_engine(f"sqlite:///{self.DB_FILE}")

        # 2. Pass this exact engine instance to CharacterManager
        self.server = CharacterManager("ACIT", self.DB_FILE, engine=self.engine)

        # 3. Create tables using this same engine
        Base.metadata.create_all(self.engine)

        # Initialize test character objects
        self.player = Player(1, "assassin")
        self.monster = Monster("dragon", "easy")

    def tearDown(self):
        """Clean up after each test"""
        # 1. Dispose the engine to close all database connections.
        if hasattr(self, "engine") and self.engine:
            self.engine.dispose()

        # 2. Remove the database file.
        if os.path.exists(self.DB_FILE):
            os.remove(self.DB_FILE)

    # --- Test Cases ---

    def test_server_valid_parameters(self):
        """010A - Valid server and database parameters"""
        # pylint: disable=protected-access
        self.assertEqual(self.server._server_name, "ACIT")
        self.assertEqual(self.server._db_filename, self.DB_FILE)

    def test_server_invalid_parameters(self):
        """010B - Invalid server or database parameters"""
        test_cases = [
            (None, self.DB_FILE, "Server Name cannot be undefined \\(None\\)\\."),
            ("", self.DB_FILE, "Server Name cannot be empty\\."),
            ("ACIT", None, "Database Name cannot be undefined \\(None\\)\\."),
            ("ACIT", "", "Database Name cannot be empty\\."),
            (1111, self.DB_FILE, "Server Name must be a string\\."),
            ("ACIT", 1111, "Database Name must be a string\\."),
        ]
        for server_name, db_filename, expected_regex in test_cases:
            with self.subTest(server_name=server_name, db_filename=db_filename):
                self.assertRaisesRegex(
                    ValueError,
                    expected_regex,
                    CharacterManager,
                    server_name,
                    db_filename,
                )

    def test_add_character_valid(self):
        """020A - Add valid character objects"""
        self.assertEqual(len(self.server.get_all()), 0)

        # Add player 1
        self.server.add_character(self.player)
        self.assertEqual(len(self.server.get_all()), 1)
        player_1_from_db = self.server.get_all()[0]
        self.assertTrue(self.server.character_exists(player_1_from_db.id))

        # Add player 2
        player_2 = Player(2, "knight")
        self.server.add_character(player_2)
        self.assertEqual(len(self.server.get_all()), 2)
        player_2_from_db = self.server.get_all()[1]
        self.assertTrue(self.server.character_exists(player_2_from_db.id))
        self.assertTrue(self.server.character_exists(player_1_from_db.id))

        # Add monster
        self.server.add_character(self.monster)
        self.assertEqual(len(self.server.get_all()), 3)
        monster_from_db = self.server.get_all()[2]
        self.assertTrue(self.server.character_exists(monster_from_db.id))

    def test_add_character_invalid(self):
        """020B - Add invalid character object"""
        test_cases = [
            (None, "Character Object cannot be undefined\\."),
            (
                "",
                "Invalid Character Object: Must be an instance of AbstractCharacter or its subclass\\.",
            ),
            (
                "String Object",
                "Invalid Character Object: Must be an instance of AbstractCharacter or its subclass\\.",
            ),
        ]
        for invalid_char_obj, expected_regex in test_cases:
            with self.subTest(invalid_char_obj=invalid_char_obj):
                self.assertRaisesRegex(
                    ValueError,
                    expected_regex,
                    self.server.add_character,
                    invalid_char_obj,
                )

    def test_character_exists_valid(self):
        """030A - Test retrieving characters from the database returns the expected Player and Monster objects."""
        self.assertFalse(self.server.character_exists(999))

        self.server.add_character(self.player)
        self.assertTrue(self.server.character_exists(1))

        self.server.add_character(self.monster)
        self.assertTrue(self.server.character_exists(2))
        self.assertTrue(self.server.character_exists(1))

    def test_character_exists_invalid(self):
        """030B - character_exists with invalid IDs"""
        test_cases = [
            (None, "ID cannot be undefined \\(None\\)\\."),
            ("", "ID cannot be empty\\."),
            ("123", "ID needs to be an integer\\."),
        ]
        for invalid_id, expected_regex in test_cases:
            with self.subTest(invalid_id=invalid_id):
                self.assertRaisesRegex(
                    ValueError, expected_regex, self.server.character_exists, invalid_id
                )

    def test_get_valid(self):
        """040A - Get valid character by ID"""
        self.server.add_character(self.monster)
        retrieved_monster = self.server.get(1)
        self.assertIsInstance(retrieved_monster, Monster)
        self.assertEqual(retrieved_monster.id, 1)
        self.assertEqual(retrieved_monster.monster_type, "dragon")

        self.server.add_character(self.player)
        retrieved_player = self.server.get(2)
        self.assertIsInstance(retrieved_player, Player)
        self.assertEqual(retrieved_player.id, 2)
        self.assertEqual(retrieved_player.job, "assassin")

    def test_get_invalid(self):
        """040B - Get character with invalid IDs"""
        test_cases = [
            (None, "ID cannot be undefined \\(None\\)\\."),
            ("", "ID cannot be empty\\."),
            ("123", "ID needs to be an integer\\."),
            (999, "Character with ID 999 does not exist\\."),
        ]
        for invalid_id, expected_regex in test_cases:
            with self.subTest(invalid_id=invalid_id):
                self.assertRaisesRegex(
                    ValueError, expected_regex, self.server.get, invalid_id
                )

    def test_get_all_valid(self):
        """050A - Get all characters valid"""
        test_server = self.server.get_all()
        self.assertEqual(test_server, [])

        self.server.add_character(self.player)
        self.server.add_character(self.monster)
        all_chars = self.server.get_all()
        self.assertEqual(len(all_chars), 2)
        self.assertIsInstance(all_chars[0], Player)
        self.assertIsInstance(all_chars[1], Monster)

    def test_get_all_by_type_valid(self):
        """060A - Get all characters by type valid"""
        self.assertEqual(len(self.server.get_all_by_type("player")), 0)
        self.assertEqual(len(self.server.get_all_by_type("monster")), 0)

        self.server.add_character(self.monster)
        self.server.add_character(self.player)
        player_two = Player(2, "knight")
        self.server.add_character(player_two)

        players = self.server.get_all_by_type("player")
        monsters = self.server.get_all_by_type("monster")

        self.assertEqual(len(players), 2)
        self.assertEqual(len(monsters), 1)
        self.assertIsInstance(players[0], Player)
        self.assertIsInstance(monsters[0], Monster)

    def test_get_all_by_type_invalid(self):
        """060B - Get all characters by invalid type"""
        test_cases = [
            (None, "Character type cannot be undefined \\(None\\)\\."),
            ("", "Character type cannot be empty\\."),
            ("Random", "Character type must be either 'player' or 'monster'\\."),
        ]
        for invalid_type, expected_regex in test_cases:
            with self.subTest(invalid_type=invalid_type):
                self.assertRaisesRegex(
                    ValueError,
                    expected_regex,
                    self.server.get_all_by_type,
                    invalid_type,
                )

    def test_update_character_valid(self):
        """070A - Update characters with valid parameters"""
        self.server.add_character(self.player)
        self.server.add_character(self.monster)

        self.server.update_character(1, "knight", 5)
        updated_player = self.server.get(1)
        self.assertEqual(updated_player.get_job(), "knight")
        self.assertEqual(updated_player.get_level(), 5)
        self.assertEqual(updated_player.health, 116)
        self.assertEqual(updated_player.damage, 32)

        self.server.update_character(2, "orc", "normal")
        updated_monster = self.server.get(2)
        self.assertEqual(updated_monster.get_monster_type(), "orc")
        self.assertEqual(updated_monster.get_monster_ai_difficulty(), "normal")
        self.assertEqual(updated_monster.health, 130)
        self.assertEqual(updated_monster.damage, 20)

    def test_update_character_invalid(self):
        """070B - Update characters with invalid parameters raises errors"""
        self.server.add_character(self.player)
        self.server.add_character(self.monster)

        test_cases_id = [
            (None, "ID cannot be undefined \\(None\\)\\."),
            ("", "ID cannot be empty"),
            ("123", "ID needs to be an integer\\."),
            (999, "Character with ID 999 does not exist\\."),
        ]
        for invalid_id, expected_regex in test_cases_id:
            with self.subTest(id_test=invalid_id):
                self.assertRaisesRegex(
                    ValueError,
                    expected_regex,
                    self.server.update_character,
                    invalid_id,
                    "knight",
                    1,
                )

        test_cases_player_params = [
            (1, None, 1, "Job/Type cannot be undefined \\(None\\)\\."),
            (1, "", 1, "Job/Type cannot be empty\\."),
            (1, 123, 1, "Job/Type must be a string\\."),
            (
                1,
                "invalid_job",
                1,
                "Player Job must be either assassin, knight, or warrior.",
            ),
            (1, "knight", None, "Level cannot be undefined \\(None\\)\\."),
            (1, "knight", "1", "Level needs to be an integer\\."),
            (1, "knight", 99, "is out of range, please enter 1-10"),
        ]
        for char_id, param1, param2, expected_regex in test_cases_player_params:
            with self.subTest(player_params=f"{param1}, {param2}"):
                self.assertRaisesRegex(
                    ValueError,
                    expected_regex,
                    self.server.update_character,
                    char_id,
                    param1,
                    param2,
                )

        test_cases_monster_params = [
            (2, None, "easy", "Job/Type cannot be undefined \\(None\\)\\."),
            (2, "", "easy", "Job/Type cannot be empty\\."),
            (2, 123, "easy", "Job/Type must be a string\\."),
            (
                2,
                "invalid_type",
                "easy",
                "Monster type must be either dragon, orc or elf",
            ),
            (2, "orc", None, "Difficulty cannot be undefined \\(None\\)\\."),
            (2, "orc", "", "Difficulty cannot be empty\\."),
            (2, "orc", 123, "Difficulty must be a string\\."),
            (
                2,
                "orc",
                "invalid_difficulty",
                "Monster AI difficulty must be either easy, normal, or hard.",
            ),
        ]
        for char_id, param1, param2, expected_regex in test_cases_monster_params:
            with self.subTest(monster_params=f"{param1}, {param2}"):
                self.assertRaisesRegex(
                    ValueError,
                    expected_regex,
                    self.server.update_character,
                    char_id,
                    param1,
                    param2,
                )

    def test_delete_character_valid(self):
        """080A - Delete characters with valid IDs successfully"""
        self.server.add_character(self.monster)
        self.server.add_character(self.player)
        self.assertEqual(len(self.server.get_all()), 2)

        self.server.delete_character(1)
        self.assertEqual(len(self.server.get_all()), 1)
        self.assertFalse(self.server.character_exists(1))
        self.assertTrue(self.server.character_exists(2))

        self.server.delete_character(2)
        self.assertEqual(len(self.server.get_all()), 0)
        self.assertFalse(self.server.character_exists(2))

    def test_delete_character_invalid(self):
        """080B - Delete characters with invalid IDs raises errors"""
        test_cases = [
            (None, "ID cannot be undefined \\(None\\)\\."),
            ("", "ID cannot be empty\\."),
            ("123", "ID needs to be an integer\\."),
            (999, "Character with ID 999 does not exist\\."),
        ]
        for invalid_id, expected_regex in test_cases:
            with self.subTest(invalid_id=invalid_id):
                self.assertRaisesRegex(
                    ValueError, expected_regex, self.server.delete_character, invalid_id
                )

    def test_get_server_name_valid(self):
        """090A - Get server name returns correct name"""
        self.assertEqual(self.server.get_server_name(), "ACIT")
        self.assertNotEqual(self.server.get_server_name(), "BCIT")

    def test_get_server_stats_valid(self):
        """100A - Get server statistics returns accurate values"""
        server_stats_no_chars = self.server.get_server_stats()
        self.assertEqual(server_stats_no_chars.total_num_characters, 0)
        self.assertEqual(server_stats_no_chars.num_monsters, 0)
        self.assertEqual(server_stats_no_chars.num_players, 0)
        self.assertEqual(server_stats_no_chars.avg_player_level, 0)
        self.assertEqual(
            server_stats_no_chars.avg_monster_ai_difficulty, "not available"
        )

        self.server.add_character(self.monster)
        self.server.add_character(self.player)
        server_stats_with_chars = self.server.get_server_stats()

        self.assertEqual(server_stats_with_chars.total_num_characters, 2)
        self.assertEqual(server_stats_with_chars.num_monsters, 1)
        self.assertEqual(server_stats_with_chars.num_players, 1)
        self.assertEqual(server_stats_with_chars.avg_player_level, 1)
        self.assertEqual(server_stats_with_chars.avg_monster_ai_difficulty, "easy")

        player_level_5 = Player(5, "warrior")
        player_level_10 = Player(10, "knight")
        monster_normal = Monster("orc", "normal")
        monster_hard = Monster("elf", "hard")

        self.server.add_character(player_level_5)
        self.server.add_character(player_level_10)
        self.server.add_character(monster_normal)
        self.server.add_character(monster_hard)

        server_stats_full = self.server.get_server_stats()

        self.assertEqual(server_stats_full.total_num_characters, 6)
        self.assertEqual(server_stats_full.num_monsters, 3)
        self.assertEqual(server_stats_full.num_players, 3)
        self.assertEqual(server_stats_full.avg_player_level, 5)
        self.assertEqual(server_stats_full.avg_monster_ai_difficulty, "normal")

    def test_get_character_details_by_type_valid(self):
        """110A - Get character details by type returns correct details"""
        self.assertEqual(
            len(self.server.get_character_details_by_type(Player.CHARACTER_TYPE)), 0
        )
        self.assertEqual(
            len(self.server.get_character_details_by_type(Monster.CHARACTER_TYPE)), 0
        )

        self.server.add_character(self.monster)
        self.server.add_character(self.player)
        player_two = Player(2, "knight")
        self.server.add_character(player_two)

        player_details = self.server.get_character_details_by_type(
            Player.CHARACTER_TYPE
        )
        monster_details = self.server.get_character_details_by_type(
            Monster.CHARACTER_TYPE
        )

        self.assertEqual(len(player_details), 2)
        self.assertEqual(len(monster_details), 1)

        self.assertIn("The player (id:", player_details[0])
        self.assertIn("is level 1 assassin", player_details[0])
        self.assertIn("The monster (id:", monster_details[0])
        self.assertIn("is easy dragon", monster_details[0])

    def test_get_character_details_by_type_invalid(self):
        """110B - Get character details by invalid type raises errors"""
        test_cases = [
            (None, "Character type cannot be undefined \\(None\\)\\."),
            ("", "Character type cannot be empty\\."),
            ("Random", "Character type must be either 'player' or 'monster'\\."),
        ]
        for invalid_type, expected_regex in test_cases:
            with self.subTest(invalid_type=invalid_type):
                self.assertRaisesRegex(
                    ValueError,
                    expected_regex,
                    self.server.get_character_details_by_type,
                    invalid_type,
                )

    def test_get_all_character_details_valid(self):
        """120A - Get all character details returns correct results"""
        details1 = self.server.get_all_character_details()
        self.assertEqual(0, len(details1))

        self.server.add_character(self.monster)
        self.server.add_character(self.player)

        details2 = self.server.get_all_character_details()
        self.assertEqual(2, len(details2))
        self.assertIn("The monster (id: 1) is easy dragon", details2)
        self.assertIn("The player (id: 2) is level 1 assassin", details2)

    def test_get_character_details_valid(self):
        """130A - Get character details by valid ID returns correct info"""
        self.server.add_character(self.monster)
        self.server.add_character(self.player)

        details1 = self.server.get_character_details(1)
        self.assertEqual(
            "The monster (id: 1) is easy dragon with 150 health and 10 damage, Position: X = 0 Y = 0",
            details1,
        )
        details2 = self.server.get_character_details(2)
        self.assertEqual(
            "The player (id: 2) is level 1 assassin with 80 health and 30 damage, Position: X = 0 Y = 0",
            details2,
        )

    def test_get_character_details_invalid(self):
        """130B - Get character details by invalid ID raises errors"""
        test_cases = [
            (None, "ID cannot be undefined \\(None\\)\\."),
            ("", "ID cannot be empty\\."),
            ("123", "ID needs to be an integer\\."),
            (999, "Character with ID 999 does not exist\\."),
        ]
        for invalid_id, expected_regex in test_cases:
            with self.subTest(invalid_id=invalid_id):
                self.assertRaisesRegex(
                    ValueError,
                    expected_regex,
                    self.server.get_character_details,
                    invalid_id,
                )


if __name__ == "__main__":
    unittest.main()
