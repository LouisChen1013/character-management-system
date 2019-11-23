import tkinter as tk
from tkinter import messagebox
import requests
import re


class AddMonsterPopup(tk.Frame):
    """ Popup Frame to Add a Monster """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        tk.Label(self, text="Monster Type:").grid(row=1, column=1)
        self.monster_type = tk.Entry(self)
        self.monster_type.grid(row=1, column=2)
        tk.Label(self, text="Monster AI Difficulty:").grid(row=2, column=1)
        self.monster_ai_difficulty = tk.Entry(self)
        self.monster_ai_difficulty.grid(row=2, column=2)
        tk.Button(self, text="Submit", command=self._submit_cb).grid(
            row=4, column=1)
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=4, column=2)

    def _submit_cb(self):
        """ Submit the Add Phone """

        # Validate the non-string data values
        if re.match("dragon|Dragon|orc|Orc|elf|Elf", self.monster_type.get()) is None:
            messagebox.showerror(
                "Error", "Monster type must be dragon, orc, or elf")
            return

        if re.match("easy|Easy|normal|Normal|hard|Hard", self.monster_ai_difficulty.get()) is None:
            messagebox.showerror(
                "Error", "Monster type must be dragon, orc, or elf")
            return

        # Create the dictionary for the JSON request body
        data = {}
        data['monster_type'] = self.monster_type.get()
        data['monster_ai_difficulty'] = self.monster_ai_difficulty.get()
        data['type'] = "monster"

        print(data)

        # Implement your code here

        """ Adds a device to the backend shop"""
        headers = {"content-type": "application/json"}
        response = requests.post(
            "http://127.0.0.1:5000/server/character", json=data, headers=headers)

        if response.status_code == 200:
            self._close_cb()
        else:
            messagebox.showerror(
                "Error", "Add Monster Request Failed" + response.text)
