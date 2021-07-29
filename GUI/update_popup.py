import tkinter as tk
from tkinter import messagebox
import requests
import re
from player_update_popup import PlayerUpdatePopup
from monster_update_popup import MonsterUpdatePopup


class UpdatePopup(tk.Frame):
    """ Popup Frame to Update Character """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        tk.Label(self, text="Update player or monster").grid(row=1, column=2)
        tk.Button(self, text="Player", command=self._player_cb).grid(
            row=3, column=1)
        tk.Button(self, text="Monster", command=self._monster_cb).grid(
            row=3, column=3)
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=5, column=2)

    def _player_cb(self):
        self._popup_win = tk.Toplevel()
        self._popup = PlayerUpdatePopup(self._popup_win, self._close_player_cb)
        self._close_cb()

    def _close_player_cb(self):
        self._popup_win.destroy()

    def _monster_cb(self):
        self._popup_win = tk.Toplevel()
        self._popup = MonsterUpdatePopup(
            self._popup_win, self._close_monster_cb)
        self._close_cb()

    def _close_monster_cb(self):
        self._popup_win.destroy()
