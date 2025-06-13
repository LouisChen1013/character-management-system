class ServerStats:
    """Statistics on Server"""

    def __init__(
        self,
        total_num_characters: int,
        num_monsters: int,
        num_players: int,
        avg_player_level: int,
        avg_monster_ai_difficulty: str,
    ):
        """Initialize the data values"""

        if not isinstance(total_num_characters, int):
            raise ValueError("Invalid number of total characters value")
        self._total_num_characters = total_num_characters

        if not isinstance(num_monsters, int):
            raise ValueError("Invalid number of monsters value")
        self._num_monsters = num_monsters

        if not isinstance(num_players, int):
            raise ValueError("Invalid number of players value")
        self._num_players = num_players

        if not isinstance(avg_player_level, int):
            raise ValueError("Invalid average player level value")
        self._avg_player_level = avg_player_level

        if not isinstance(avg_monster_ai_difficulty, str):
            raise ValueError("Invalid average monster AI difficulty value")
        self._avg_monster_ai_difficulty = avg_monster_ai_difficulty

    @property
    def total_num_characters(self) -> int:
        """Returns the total number of characters."""
        return self._total_num_characters

    @property
    def num_monsters(self) -> int:
        """Returns the number of monster characters."""
        return self._num_monsters

    @property
    def num_players(self) -> int:
        """Returns the number of players."""
        return self._num_players

    @property
    def avg_player_level(self) -> int:
        """Returns the average level of players."""
        return self._avg_player_level

    @property
    def avg_monster_ai_difficulty(self) -> str:
        """Returns the average monster AI difficulty."""
        return self._avg_monster_ai_difficulty

    def to_dict(self) -> dict:
        """Returns a dictionary representation of server stats."""
        return {
            "total_num_characters": self.total_num_characters,
            "num_monsters": self.num_monsters,
            "num_players": self.num_players,
            "avg_player_level": self.avg_player_level,
            "avg_monster_ai_difficulty": self.avg_monster_ai_difficulty,
        }
