import unittest
import inspect
from monster import Monster


class TestMonster(unittest.TestCase):
    """ Unit Test for Monster Class """

    def setUp(self):
        """ Initialize fixtures """

        self.logMonster()
        self.monster = Monster("dragon", "easy")
        self.assertIsNotNone(self.monster)

    def test_constructor_valid(self):
        """ Test 010A - Valid Construction"""

        self.assertIsInstance(self.monster, Monster)

    def test_constructor_invalid(self):
        """ Test 010B - Invalid Construction """

        self.assertRaisesRegex(
            ValueError, "Monster type cannot be undefined", Monster, None, "easy")
        self.assertRaisesRegex(
            ValueError, "Monster type cannot be empty", Monster, "", "easy")
        self.assertRaisesRegex(
            ValueError, "Monster AI difficulty cannot be undefined", Monster, "dragon", None)
        self.assertRaisesRegex(
            ValueError, "Monster AI difficulty cannot be empty", Monster, "dragon", "")

        self.assertNotIn("Human".lower(), Monster.MONSTER_TYPE)
        self.assertNotIn("Medium".lower(), Monster.MONSTER_AI_DIFFICULTY)

    def test_set_monster_type_valid(self):
        """ Test 020A - Set valid monster types"""

        self.monster.set_monster_type("dragon")
        self.assertEqual("dragon", self.monster.get_monster_type())

        self.monster.set_monster_type("orc")
        self.assertEqual("orc", self.monster.get_monster_type())

        self.monster.set_monster_type("elf")
        self.assertEqual("elf", self.monster.get_monster_type())

    def test_set_monster_type_invalid(self):
        """ Test 020B - Set invalid monster types"""

        self.assertRaisesRegex(
            ValueError, "Monster type must be either dragon, orc, or elf", self.monster.set_monster_type, "Human".lower())
        self.assertRaisesRegex(
            ValueError, "Monster type cannot be undefined", self.monster.set_monster_type, None)
        self.assertRaisesRegex(
            ValueError, "Monster type cannot be empty", self.monster.set_monster_type, "")

    def test_get_monster_type(self):
        """ Test 030A - Get valid monster types"""

        self.assertEqual(self.monster.get_monster_type(), "dragon")

        self.monster.set_monster_type("dragon")
        self.assertEqual(self.monster.get_monster_type(), "dragon")

        self.monster.set_monster_type("orc")
        self.assertEqual(self.monster.get_monster_type(), "orc")

    def test_set_monster_ai_difficulty_valid(self):
        """ Test 040A - Set valid monster ai difficulty"""

        self.monster.set_monster_ai_difficulty("easy")
        self.assertEqual("easy", self.monster.get_monster_ai_difficulty())

        self.monster.set_monster_ai_difficulty("normal")
        self.assertEqual("normal", self.monster.get_monster_ai_difficulty())

        self.monster.set_monster_ai_difficulty("hard")
        self.assertEqual("hard", self.monster.get_monster_ai_difficulty())

    def test_set_monster_ai_difficulty_invalid(self):
        """ Test 040B - Set invalid monster ai difficulty"""

        self.assertRaisesRegex(
            ValueError, "Monster AI difficulty must be either easy, normal, or hard", self.monster.set_monster_ai_difficulty, "Medium".lower())
        self.assertRaisesRegex(
            ValueError, "Monster AI difficulty cannot be undefined", self.monster.set_monster_ai_difficulty, None)
        self.assertRaisesRegex(
            ValueError, "Monster AI difficulty cannot be empty", self.monster.set_monster_ai_difficulty, "")

    def test_get_monster_ai_difficulty(self):
        """ Test 050A - Get valid monster ai difficulty"""

        self.assertEqual(self.monster.get_monster_ai_difficulty(), "easy")
        # change same
        self.monster.set_monster_ai_difficulty("easy")
        self.assertEqual(self.monster.get_monster_ai_difficulty(), "easy")
        # change different
        self.monster.set_monster_ai_difficulty("normal")
        self.assertEqual(self.monster.get_monster_ai_difficulty(), "normal")

    def test_get_details(self):
        """ Test 060A - Get valid details"""

        self.assertEqual(
            "The monster is easy dragon with 150 health and 10 damage, Position: X = 0 Y = 0", self.monster.get_details())
        self.monster.set_monster_ai_difficulty("normal")
        self.assertEqual(
            "The monster is normal dragon with 150 health and 20 damage, Position: X = 0 Y = 0", self.monster.get_details())
        self.monster.set_monster_type("orc")
        self.assertEqual(
            "The monster is normal orc with 130 health and 20 damage, Position: X = 0 Y = 0", self.monster.get_details())
        self.monster.set_monster_ai_difficulty("hard")
        self.monster.set_monster_type("elf")
        self.assertEqual(
            "The monster is hard elf with 110 health and 30 damage, Position: X = 0 Y = 0", self.monster.get_details())

    def get_type(self):
        """ Test 070A - Get valid type"""
        self.assertEqual("monster", self.monster.get_type())

    def tearDown(self):
        """" Tear down """
        self.logMonster()

    def logMonster(self):
        currentTest = self.id().split('.')[-1]
        callingFunction = inspect.stack()[1][3]
        print('in %s - %s()' % (currentTest, callingFunction))


if __name__ == "__main__":
    unittest.main()
