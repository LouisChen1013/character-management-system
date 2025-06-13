import tkinter as tk
from player_update_popup import PlayerUpdatePopup
from monster_update_popup import MonsterUpdatePopup


class UpdatePopup(tk.Frame):
    """Popup Frame to Choose Character Type to Update"""

    def __init__(self, parent, close_callback):
        super().__init__(parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2, padx=10, pady=10)

        tk.Label(self, text="Update Player or Monster").grid(
            row=1, column=1, columnspan=3, pady=10
        )

        tk.Button(self, text="Player", command=self._open_player_popup, width=15).grid(
            row=3, column=1, padx=10, pady=5
        )
        tk.Button(
            self, text="Monster", command=self._open_monster_popup, width=15
        ).grid(row=3, column=3, padx=10, pady=5)
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=5, column=2, pady=15
        )

        self._popup_win = None

    def _open_player_popup(self):
        self._popup_win = tk.Toplevel()
        PlayerUpdatePopup(self._popup_win, self._close_popup_and_self)

    def _open_monster_popup(self):
        self._popup_win = tk.Toplevel()
        MonsterUpdatePopup(self._popup_win, self._close_popup_and_self)

    def _close_popup_and_self(self):
        if self._popup_win:
            self._popup_win.destroy()
        self._close_cb()
