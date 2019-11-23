import tkinter as tk
import requests
from add_monster_popup import AddMonsterPopup
from add_player_popup import AddPlayerPopup
from update_popup import UpdatePopup
from delete_popup import DeletePopup


class MainAppController(tk.Frame):
    """ Main Application for GUI """

    def __init__(self, parent):
        """ Initialize Main Application """
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="Characters in the Server").grid(row=1, column=2)
        self._characters_listbox = tk.Listbox(self, width=100)
        self._characters_listbox.grid(row=2, column=1, columnspan=5)

        self._players_listbox
        self._monsters_listbox


        tk.Button(self, text="Add Player",
                  command=self._add_player).grid(row=3, column=1)
        tk.Button(self, text="Add Monster",
                  command=self._add_monster).grid(row=3, column=2)
        tk.Button(self, text="Update Character",
                  command=self._update_character).grid(row=3, column=3)
        tk.Button(self, text="Delete Character",
                  command=self._delete_character).grid(row=3, column=4)
        tk.Button(self, text="Quit", command=self._quit_callback).grid(
            row=4, column=2)

        self._update_devices_list()

    def _add_player(self):
        """ Add Player Popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddPlayerPopup(self._popup_win, self._close_player_cb)

    def _close_player_cb(self):
        """ Close Add Phone Popup """
        self._popup_win.destroy()
        self._update_characters_list()

    def _add_monster(self):
        """ Add Tablet Popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddMonsterPopup(self._popup_win, self._close_monster_cb)

    def _close_monster_cb(self):
        """ Close Add Monster Popup """
        self._popup_win.destroy()
        self._update_characters_list()

    def _delete_character(self):
        """ Delete Character Popup """
        self._popup_win = tk.Toplevel()
        self._popup = DeletePopup(self._popup_win, self._close_delete_cb)

    def _close_delete_cb(self):
        """ Close Delete Character Popup """
        self._popup_win.destroy()
        self._update_devices_list()

    def _update_character(self):
        """ Update Character Popup """
        self._popup_win = tk.Toplevel()
        self._popup = UpdatePopup(self._popup_win, self._close_update_cb)

    def _close_update_cb(self):
        """ Close Update Repair Popup """
        self._popup_win.destroy()
        self._update_devices_list()

    def _quit_callback(self):
        """ Quit """
        self.quit()

    def _toggle_player(self):

    

    def _update_devices_list(self):
        """ Update the List of Character Descriptions """

        # Tablet
        self._characters_listbox.delete(0, tk.END)

        response = requests.get(
            "http://127.0.0.1:5000/repairshop/devices/descriptions/player")
        player_descs = response.json()
        for player_desc in player_descs:
            self._characters_listbox.insert(tk.END, player_desc)

        # Monster
        response = requests.get(
            "http://127.0.0.1:5000/repairshop/devices/descriptions/monster")
        monster_descs = response.json()
        for monster_desc in monster_descs:
            self._characters_listbox.insert(tk.END, monster_desc)


if __name__ == "__main__":
    root = tk.Tk()
    MainAppController(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()
