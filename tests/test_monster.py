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
from monster import Monster
from character_manager import CharacterManager


class TestMonster(unittest.TestCase):
    """Unit Test for Monster Class"""

    DB_FILE = "test_characters.sqlite"

    def setUp(self):
        """Initialize fixtures"""
        self.log_monster()
        self.monster = Monster("dragon", "easy")

        self.engine = create_engine(f"sqlite:///{self.DB_FILE}")
        self.server = CharacterManager("ACIT", self.DB_FILE, engine=self.engine)

        Base.metadata.create_all(self.engine)

        TestMonster.server = self.server

        self.assertIsNotNone(self.monster)

    def test_constructor_valid(self):
        """Test 010A - Valid Monster Constructor"""
        self.assertIsInstance(self.monster, Monster)

    def test_constructor_invalid(self):
        """Test 010B - Invalid Monster Constructor"""
        with self.assertRaisesRegex(ValueError, "Monster type must be a string."):
            Monster(None, "easy")
        with self.assertRaisesRegex(ValueError, "Monster type cannot be empty."):
            Monster("", "easy")
        with self.assertRaisesRegex(
            ValueError, "Monster AI difficulty must be a string."
        ):
            Monster("dragon", None)
        with self.assertRaisesRegex(
            ValueError, "Monster AI difficulty cannot be empty."
        ):
            Monster("dragon", "")

    def test_set_monster_type_valid(self):
        """Test 020A - Valid set_monster_type"""
        for mtype in ["dragon", "orc", "elf"]:
            self.monster.set_monster_type(mtype)
            self.assertEqual(mtype, self.monster.get_monster_type())

    def test_set_monster_type_invalid(self):
        """Test 020B - Invalid set_monster_type"""
        with self.assertRaisesRegex(
            ValueError, "Monster type must be either dragon, orc or elf"
        ):
            self.monster.set_monster_type("human")
        with self.assertRaisesRegex(ValueError, "Monster type must be a string."):
            self.monster.set_monster_type(None)
        with self.assertRaisesRegex(ValueError, "Monster type cannot be empty."):
            self.monster.set_monster_type("")

    def test_get_monster_type(self):
        """Test 030A - Get monster type"""
        self.assertEqual("dragon", self.monster.get_monster_type())
        self.monster.set_monster_type("orc")
        self.assertEqual("orc", self.monster.get_monster_type())

    def test_set_monster_ai_difficulty_valid(self):
        """Test 040A - Valid set_monster_ai_difficulty"""
        for diff in ["easy", "normal", "hard"]:
            self.monster.set_monster_ai_difficulty(diff)
            self.assertEqual(diff, self.monster.get_monster_ai_difficulty())

    def test_set_monster_ai_difficulty_invalid(self):
        """Test 040B - Invalid set_monster_ai_difficulty"""
        with self.assertRaisesRegex(
            ValueError, "Monster AI difficulty must be either easy, normal, or hard."
        ):
            self.monster.set_monster_ai_difficulty("medium")
        with self.assertRaisesRegex(
            ValueError, "Monster AI difficulty must be a string."
        ):
            self.monster.set_monster_ai_difficulty(None)
        with self.assertRaisesRegex(
            ValueError, "Monster AI difficulty cannot be empty."
        ):
            self.monster.set_monster_ai_difficulty("")

    def test_get_monster_ai_difficulty(self):
        """Test 050A - Get monster AI difficulty"""
        self.assertEqual("easy", self.monster.get_monster_ai_difficulty())
        self.monster.set_monster_ai_difficulty("normal")
        self.assertEqual("normal", self.monster.get_monster_ai_difficulty())

    def test_get_details(self):
        """Test 060A - Monster get_details returns description"""
        self.server.add_character(self.monster)
        refreshed_monster = self.server.get_all()[0]
        self.assertIn("The monster", refreshed_monster.get_details())

    def test_get_type(self):
        """Test 070A - Get monster type name"""
        self.assertEqual("monster", self.monster.get_type())

    def test_to_dict(self):
        """Test 080A - Valid to_dict: ensures Monster object serializes correctly"""
        self.server.add_character(self.monster)
        refreshed_monster = self.server.get_all()[0]
        monster_dict = refreshed_monster.to_dict()

        self.assertEqual(monster_dict["id"], 1)
        self.assertEqual(monster_dict["health"], 150)
        self.assertEqual(monster_dict["damage"], 10)
        self.assertEqual(monster_dict["position"], [0, 0])
        self.assertTrue(monster_dict["alive"])
        self.assertEqual(monster_dict["monster_ai_difficulty"], "easy")
        self.assertEqual(monster_dict["monster_type"], "dragon")
        self.assertEqual(monster_dict["type"], "monster")

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
        self.log_monster()

    def log_monster(self):
        """Prints current test method and its calling function for debug trace."""
        current_test = self.id().split(".")[-1]
        calling_function = inspect.stack()[1][3]
        print(f"in {current_test} - {calling_function}()")


if __name__ == "__main__":
    unittest.main()
