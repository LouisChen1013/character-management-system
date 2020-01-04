import tkinter as tk
from tkinter import messagebox
import requests
import re


class PlayerUpdatePopup(tk.Frame):
    """ Popup Frame to Update a Character """

    def __init__(self, parent, selected_id, level, job, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        tk.Label(self, text="ID:").grid(row=1, column=1)
        tk.Label(self, text=selected_id).grid(row=1, column=2)
        tk.Label(self, text="Level:").grid(row=2, column=1)
        self._player_level = tk.Entry(self)
        self._player_level.grid(row=2, column=2)
        tk.Label(self, text="Job:").grid(row=3, column=1)
        self._job = tk.Entry(self)
        self._job.grid(row=3, column=2)
        tk.Button(self, text="Submit", command=self._submit_cb).grid(row=7, column=1)
        tk.Button(self, text="Close", command=self._close_cb).grid(row=7, column=2)

        self._selected_id = selected_id
        self._player_level.insert(0, level)
        self._job.insert(0, job)

    def _submit_cb(self):
        """ Submit Character Update """

        # Validate the non-string data values
        if self._player_level.get() == "":
            messagebox.showerror(
                "Error", "Player level must be a valid integer")
            return

        """ Update a character to the backend server"""
        data = {}
        data['player_level'] = int(self._player_level.get())
        data['job'] = self._job.get()

        headers = {"content-type": "application/json"}
        response = requests.put(
            "http://127.0.0.1:5000/server/character/" + str(self._selected_id), json=data, headers=headers)

        if response.status_code == 200:
            self._close_cb()
        else:
            messagebox.showerror(
                "Error", "Unable to Upadte the Character: " + response.text)

        self._close_cb()
