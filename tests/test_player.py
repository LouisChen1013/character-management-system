import os
import sys
import unittest
import inspect
from sqlalchemy import create_engine

# Setup path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from base import Base
from player import Player
from character_manager import CharacterManager


class TestPlayer(unittest.TestCase):
    """Unit Test for Player Class"""

    DB_FILE = "test_characters.sqlite"

    def setUp(self):
        """Initialize fixtures"""
        self.log_player()
        self.player = Player(2, "assassin")

        self.engine = create_engine(f"sqlite:///{self.DB_FILE}")
        self.server = CharacterManager("ACIT", self.DB_FILE, engine=self.engine)

        Base.metadata.create_all(self.engine)

        TestPlayer.server = self.server

        self.assertIsNotNone(self.player)

    def test_constructor_valid(self):
        """Test 010A - Valid constructor: creates a Player instance successfully"""
        self.log_player()
        self.assertIsInstance(self.player, Player)

    def test_constructor_invalid(self):
        """Test 010B - Invalid constructor: checks for level/job input validation errors"""
        self.log_player()
        with self.assertRaisesRegex(ValueError, "Player Level cannot be undefined."):
            Player(None, "assassin")
        with self.assertRaisesRegex(ValueError, "Player Level cannot be empty."):
            Player("", "assassin")
        with self.assertRaisesRegex(ValueError, "Player Job must be a string."):
            Player(2, None)
        with self.assertRaisesRegex(ValueError, "Player Job cannot be empty."):
            Player(2, "")

    def test_set_level_valid(self):
        """Test 020A - Valid set_level: updates the level correctly"""
        self.log_player()
        for level in [2, 5, 10]:
            self.player.set_level(level)
            self.assertEqual(level, self.player.get_level())

    def test_set_level_invalid(self):
        """Test 020B - Invalid set_level: level out of range or invalid input"""
        self.log_player()
        with self.assertRaisesRegex(ValueError, "Player Level is out of range."):
            self.player.set_level(20)
        with self.assertRaisesRegex(ValueError, "Player Level cannot be undefined."):
            self.player.set_level(None)
        with self.assertRaisesRegex(ValueError, "Player Level cannot be empty."):
            self.player.set_level("")

    def test_get_level(self):
        """Test 030A - Get level: verifies returned level matches expected"""
        self.log_player()
        self.assertEqual(self.player.get_level(), 2)
        self.player.set_level(4)
        self.assertEqual(self.player.get_level(), 4)

    def test_set_job_valid(self):
        """Test 040A - Valid set_job: updates the job correctly"""
        self.log_player()
        for job in ["knight", "assassin", "warrior"]:
            self.player.set_job(job)
            self.assertEqual(job, self.player.get_job())

    def test_set_job_invalid(self):
        """Test 040B - Invalid set_job: job not in valid set or invalid input"""
        self.log_player()
        with self.assertRaisesRegex(
            ValueError, "Player Job must be either assassin, knight, or warrior."
        ):
            self.player.set_job("thief")
        with self.assertRaisesRegex(ValueError, "Player Job must be a string."):
            self.player.set_job(None)
        with self.assertRaisesRegex(ValueError, "Player Job cannot be empty."):
            self.player.set_job("")

    def test_get_job(self):
        """Test 050A - Get job: verifies returned job matches expected"""
        self.log_player()
        self.assertEqual("assassin", self.player.get_job())
        self.player.set_job("warrior")
        self.assertEqual("warrior", self.player.get_job())

    def test_get_details(self):
        """Test 060A - Valid get_details: returns correct player string summary"""
        self.log_player()
        self.server.add_character(self.player)
        refreshed_player = self.server.get_all()[0]

        self.assertIn("The player", refreshed_player.get_details())

    def test_get_type(self):
        """Test 070A - Get type: confirms the type is 'player'"""
        self.log_player()
        self.assertEqual("player", self.player.get_type())

    def test_to_dict(self):
        """Test 080A - Valid to_dict: ensures Player object serializes correctly"""
        self.log_player()
        self.server.add_character(self.player)
        refreshed_player = self.server.get_all()[0]
        player_dict = refreshed_player.to_dict()

        self.assertEqual(player_dict["id"], 1)
        self.assertEqual(player_dict["health"], 84)
        self.assertEqual(player_dict["damage"], 33)
        self.assertEqual(player_dict["position"], [0, 0])
        self.assertTrue(player_dict["alive"])
        self.assertEqual(player_dict["player_level"], 2)
        self.assertEqual(player_dict["job"], "assassin")
        self.assertEqual(player_dict["type"], "player")

    def tearDown(self):
        """Clean up after each test"""
        if os.path.exists("test_characters.sqlite"):
            try:
                # pylint: disable=protected-access
                session = self.server._db_session_factory()
                session.close()
                self.server._engine.dispose()
                os.remove("test_characters.sqlite")
            except Exception as e:
                print("Cleanup failed:", e)
        self.log_player()

    def log_player(self):
        """Prints current test method and its calling function for debug trace."""
        current_test = self.id().split(".")[-1]
        calling_function = inspect.stack()[1][3]
        print(f"in {current_test} - {calling_function}()")


if __name__ == "__main__":
    unittest.main()
