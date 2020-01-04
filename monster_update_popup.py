import tkinter as tk
from tkinter import messagebox
import requests
import re


class MonsterUpdatePopup(tk.Frame):
    """ Popup Frame to Complete a Repair """

    def __init__(self, parent, selected_id, difficulty, monster_type, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        tk.Label(self, text="ID:").grid(row=1, column=1)
        tk.Label(self, text=selected_id).grid(row=1, column=2)
        tk.Label(self, text="Monster Type:").grid(row=2, column=1)
        self._monster_type = tk.Entry(self)
        self._monster_type.grid(row=2, column=2)
        tk.Label(self, text="Monster AI Difficulty:").grid(row=3, column=1)
        self._monster_ai_difficulty = tk.Entry(self)
        self._monster_ai_difficulty.grid(row=3, column=2)
        tk.Button(self, text="Submit", command=self._submit_cb).grid(
            row=7, column=1)
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=7, column=2)

        self._selected_id = selected_id
        self._monster_type.insert(0, monster_type)
        self._monster_ai_difficulty.insert(0, difficulty)

    def _submit_cb(self):
        """ Submit Character Update """


        """ Update a character to the backend server"""
        data = {}
        data['monster_type'] = self._monster_type.get()
        data['monster_ai_difficulty'] = self._monster_ai_difficulty.get()

        headers = {"content-type": "application/json"}
        response = requests.put(
            "http://127.0.0.1:5000/server/character/" + str(self._selected_id), json=data, headers=headers)

        if response.status_code == 200:
            self._close_cb()
        else:
            messagebox.showerror(
                "Error", "Unable to Upadte the Character: " + response.text)

        self._close_cb()
