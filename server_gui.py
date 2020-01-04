import tkinter as tk
import requests
from tkinter import messagebox
from add_monster_popup import AddMonsterPopup
from add_player_popup import AddPlayerPopup
from player_update_popup import PlayerUpdatePopup
from monster_update_popup import MonsterUpdatePopup
from tkinter.messagebox import showinfo
import json


class MainAppController(tk.Frame):
    """ Main Application for GUI """

    def __init__(self, parent):
        """ Initialize Main Application """
        self._total_num_characters = tk.IntVar()
        self._num_monsters = tk.IntVar()
        self._num_players = tk.IntVar()
        self._avg_player_level = tk.IntVar()
        self._avg_monster_ai_difficulty = tk.StringVar()

        tk.Frame.__init__(self, parent)

        tk.Label(self, text="Characters in the Server").grid(row=1, column=2)
        self._characters_listbox = tk.Listbox(self, width=100)
        self._characters_listbox.grid(row=2, column=1, columnspan=5)
        tk.Button(self, text="Show All Character",
                  command=lambda: [self._server_stats(), self._update_characters_list()]).grid(row=3, column=1)
        tk.Button(self, text="Show Player",
                  command=self._toggle_player).grid(row=3, column=2)
        tk.Button(self, text="Show Monster",
                  command=self._toggle_monster).grid(row=3, column=3)
        tk.Button(self, text="Show Details",
                  command=self._show_details).grid(row=3, column=4)
        tk.Button(self, text="Add Player",
                  command=self._add_player).grid(row=4, column=1)
        tk.Button(self, text="Add Monster",
                  command=self._add_monster).grid(row=4, column=2)
        tk.Button(self, text="Update Character",
                  command=self._update_character).grid(row=4, column=3)
        tk.Button(self, text="Delete Character",
                  command=self._delete_character).grid(row=4, column=4)
        tk.Button(self, text="Quit", command=self._quit_callback).grid(
            row=5, column=2, columnspan=2)

        self._total_num_characters_label = tk.Label(
            self, text="Total Character:")
        self._total_num_characters_label.grid(row=6, column=2)
        self._total_num_characters_text = tk.Label(
            self, textvariable=self._total_num_characters)
        self._total_num_characters_text.grid(row=6, column=3)

        self._total_num_monsters_label = tk.Label(self, text="Total Monsters:")
        self._total_num_monsters_label.grid(row=7, column=2)
        self._total_num_monsters_text = tk.Label(
            self, textvariable=self._num_monsters)
        self._total_num_monsters_text.grid(row=7, column=3)

        self._total_num_players_label = tk.Label(self, text="Total Players:")
        self._total_num_players_label.grid(row=8, column=2)
        self._total_num_players_text = tk.Label(
            self, textvariable=self._num_players)
        self._total_num_players_text.grid(row=8, column=3)

        self._avg_player_level_label = tk.Label(
            self, text="Average Player Level:")
        self._avg_player_level_label.grid(row=9, column=2)
        self._avg_player_level_text = tk.Label(
            self, textvariable=self._avg_player_level)
        self._avg_player_level_text.grid(row=9, column=3)

        self._avg_monster_ai_difficulty_label = tk.Label(
            self, text="Average Monster AI Difficulty:")
        self._avg_monster_ai_difficulty_label.grid(row=10, column=2)
        self._avg_monster_ai_difficulty_text = tk.Label(
            self, textvariable=self._avg_monster_ai_difficulty)
        self._avg_monster_ai_difficulty_text.grid(row=10, column=3)

        self._update_characters_list()
        self._server_stats()

    def _add_player(self):
        """ Add Player Popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddPlayerPopup(self._popup_win, self._close_player_cb)

    def _close_player_cb(self):
        """ Close Add Player Popup """
        self._popup_win.destroy()
        self._update_characters_list()
        self._server_stats()

    def _add_monster(self):
        """ Add Monster Popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddMonsterPopup(self._popup_win, self._close_monster_cb)

    def _close_monster_cb(self):
        """ Close Add Monster Popup """
        self._popup_win.destroy()
        self._update_characters_list()
        self._server_stats()


    def _update_character(self):
        """ Upadte the Selected Character """
        selected = self._characters_listbox.curselection()
        if selected is None or len(selected) == 0:
            messagebox.showwarning(
                "Warning", "No character selected to update.")
            return

        selection = str(self._characters_listbox.get(selected))
        nums = [int(s) for s in selection.split() if s.isdigit()]
        selected_id = nums[0]
        job_type = selection.split()[-1]
        if "player" in selection:
            level = nums[1]
            self._popup_win = tk.Toplevel()
            self._popup = PlayerUpdatePopup(self._popup_win, selected_id, level, job_type, self._close_update_cb)
        else:
            difficulty = selection.split()[-2]
            self._popup_win = tk.Toplevel()
            self._popup = MonsterUpdatePopup(self._popup_win, selected_id, difficulty, job_type, self._close_update_cb)

    def _close_update_cb(self):
        """ Close Update Character Popup """
        self._popup_win.destroy()
        self._update_characters_list()
        self._server_stats()

    def _show_details(self):
        """ Display a Character Detail """

        selected = self._characters_listbox.curselection()
        if selected is None or len(selected) == 0:
            messagebox.showwarning(
                "Warning", "No character selected to show details.")
            return

        selection = str(self._characters_listbox.get(selected)) 
        nums = [int(s) for s in selection.split() if s.isdigit()]
        selected_id = nums[0]
        url = "http://127.0.0.1:5000/server/characters/details/" + str(selected_id)
        response = requests.get(url)

        if response.status_code != 200:
            messagebox.showwarning(
                "Warning", "Could not retrieve the characters.")
            return
        character_stats = response.json()
        showinfo("Character Stats", character_stats)

    def _delete_character(self):
        """ Deletes the Selected Character """
        selected = self._characters_listbox.curselection()
        if selected is None or len(selected) == 0:
            messagebox.showwarning(
                "Warning", "No character selected to delete.")
            return

        selection = str(self._characters_listbox.get(selected
            )) 
        nums = [int(s) for s in selection.split() if s.isdigit()]
        selected_id = nums[0]
        result = messagebox.askyesno(
            "Confirm", "Are you sure you want to delete the character?")
        if result:
            response = requests.delete(
                "http://127.0.0.1:5000/server/characters/" + str(selected_id))
            self._update_characters_list()
            self._server_stats()

    def _quit_callback(self):
        """ Quit """
        self.quit()

    def _toggle_player(self):
        """ Display Player Listbox """
        self._characters_listbox.delete(0, tk.END)

        self._forgot_stats()

        self._total_num_players_label = tk.Label(self, text="Total Players:")
        self._total_num_players_label.grid(row=6, column=2)
        self._total_num_players_text = tk.Label(
            self, textvariable=self._num_players)
        self._total_num_players_text.grid(row=6, column=3)

        self._avg_player_level_label = tk.Label(
            self, text="Average Player Level:")
        self._avg_player_level_label.grid(row=7, column=2)
        self._avg_player_level_text = tk.Label(
            self, textvariable=self._avg_player_level)
        self._avg_player_level_text.grid(row=7, column=3)

        # Player
        response = requests.get(
            "http://127.0.0.1:5000/server/characters/all/player")

        if response.status_code != 200:
            messagebox.showwarning(
                "Warning", "Could not retrieve the characters.")
            return

        player_descs = response.json()
        for player_desc in player_descs:
            self._characters_listbox.insert(tk.END, player_desc)

    def _toggle_monster(self):
        """ Display Monster Listbox """
        self._characters_listbox.delete(0, tk.END)

        self._forgot_stats()

        self._total_num_monsters_label = tk.Label(self, text="Total Monsters:")
        self._total_num_monsters_label.grid(row=6, column=2)
        self._total_num_monsters_text = tk.Label(
            self, textvariable=self._num_monsters)
        self._total_num_monsters_text.grid(row=6, column=3)

        self._avg_monster_ai_difficulty_label = tk.Label(
            self, text="Average Monster AI Difficulty:")
        self._avg_monster_ai_difficulty_label.grid(row=7, column=2)
        self._avg_monster_ai_difficulty_text = tk.Label(
            self, textvariable=self._avg_monster_ai_difficulty)
        self._avg_monster_ai_difficulty_text.grid(row=7, column=3)

        # Monster
        response = requests.get(
            "http://127.0.0.1:5000/server/characters/all/monster")

        if response.status_code != 200:
            messagebox.showwarning(
                "Warning", "Could not retrieve the characters.")
            return

        monster_descs = response.json()
        for monster_desc in monster_descs:
            self._characters_listbox.insert(tk.END, monster_desc)

    def _update_characters_list(self):
        """ Update the List of Character Descriptions """

        self._characters_listbox.delete(0, tk.END)

        # All Characters
        response = requests.get(
            "http://127.0.0.1:5000/server/characters/all_details")

        if response.status_code != 200:
            messagebox.showwarning(
                "Warning", "Could not retrieve the characters.")
            return

        character_descs = response.json()
        for character_desc in character_descs:
            self._characters_listbox.insert(tk.END, character_desc)

    def _server_stats(self):
        """ Show Server Stats """

        self._forgot_stats()

        response = requests.get("http://127.0.0.1:5000/server/serverstats")

        if response.status_code != 200:
            messagebox.showwarning("Warning", "Could not retrieve the stats.")
            return

        stats = response.json()

        self._total_num_characters.set(stats["total_num_characters"])
        self._num_monsters.set(stats["num_monsters"])
        self._num_players.set(stats["num_players"])
        self._avg_player_level.set(stats["avg_player_level"])
        self._avg_monster_ai_difficulty.set(stats["avg_monster_ai_difficulty"])

        self._total_num_characters_label = tk.Label(
            self, text="Total Character:")
        self._total_num_characters_label.grid(row=6, column=2)
        self._total_num_characters_text = tk.Label(
            self, textvariable=self._total_num_characters)
        self._total_num_characters_text.grid(row=6, column=3)

        self._total_num_monsters_label = tk.Label(self, text="Total Monsters:")
        self._total_num_monsters_label.grid(row=7, column=2)
        self._total_num_monsters_text = tk.Label(
            self, textvariable=self._num_monsters)
        self._total_num_monsters_text.grid(row=7, column=3)

        self._total_num_players_label = tk.Label(self, text="Total Players:")
        self._total_num_players_label.grid(row=8, column=2)
        self._total_num_players_text = tk.Label(
            self, textvariable=self._num_players)
        self._total_num_players_text.grid(row=8, column=3)

        self._avg_player_level_label = tk.Label(
            self, text="Average Player Level:")
        self._avg_player_level_label.grid(row=9, column=2)
        self._avg_player_level_text = tk.Label(
            self, textvariable=self._avg_player_level)
        self._avg_player_level_text.grid(row=9, column=3)

        self._avg_monster_ai_difficulty_label = tk.Label(
            self, text="Average Monster AI Difficulty:")
        self._avg_monster_ai_difficulty_label.grid(row=10, column=2)
        self._avg_monster_ai_difficulty_text = tk.Label(
            self, textvariable=self._avg_monster_ai_difficulty)
        self._avg_monster_ai_difficulty_text.grid(row=10, column=3)

    def _forgot_stats(self):
        """ Hide Server Stats """

        self._total_num_characters_label.grid_forget()
        self._total_num_characters_text.grid_forget()
        self._total_num_players_label.grid_forget()
        self._total_num_players_text.grid_forget()
        self._avg_player_level_label.grid_forget()
        self._avg_player_level_text.grid_forget()
        self._total_num_monsters_label.grid_forget()
        self._total_num_monsters_text.grid_forget()
        self._avg_monster_ai_difficulty_label.grid_forget()
        self._avg_monster_ai_difficulty_text.grid_forget()


if __name__ == "__main__":
    root = tk.Tk()
    MainAppController(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()
