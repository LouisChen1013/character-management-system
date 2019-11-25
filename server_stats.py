class ServerStats:
    """ Statistics on Server """

    def __init__(self, total_num_characters, num_monsters, num_players, avg_player_level, avg_monster_ai_difficulty):
        """ Initialize the data values """

        if total_num_characters is None or type(total_num_characters) != int:
            raise ValueError(
                "Invalid number of total characters value")
        self._total_num_characters = total_num_characters

        if num_monsters is None or type(num_monsters) != int:
            raise ValueError("Invalid number of monsters value")
        self._num_monsters = num_monsters

        if num_players is None or type(num_players) != int:
            raise ValueError("Invalid number of players value")
        self._num_players = num_players

        if avg_player_level is None or type(avg_player_level) != int:
            raise ValueError("Invalid average player level value")
        self._avg_player_level = avg_player_level

        if avg_monster_ai_difficulty is None or type(avg_monster_ai_difficulty) != str:
            raise ValueError("Invalid average monster ai difficulty value")
        self._avg_monster_ai_difficulty = avg_monster_ai_difficulty

    def get_total_num_characters(self):
        """ Returns the total number of characters """

        return self._total_num_characters

    def get_num_monsters(self):
        """ Returns the number of monster characters """

        return self._num_monsters

    def get_num_players(self):
        """ Returns the number of players """

        return self._num_players

    def get_avg_player_level(self):
        """ Returns the average level of players """

        return self._avg_player_level

    def get_avg_monster_ai_difficulty(self):
        """Returns the average monster ai difficulty """

        return self._avg_monster_ai_difficulty

    def to_dict(self):
        """ Returns a dictionary representation of server stats """

        dict = {}
        dict['total_num_characters'] = self.get_total_num_characters()
        dict['num_monsters'] = self.get_num_monsters()
        dict['num_players'] = self.get_num_players()
        dict['avg_player_level'] = self.get_avg_player_level()
        dict['avg_monster_ai_difficulty'] = self.get_avg_monster_ai_difficulty()

        return dict
