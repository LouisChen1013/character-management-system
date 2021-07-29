import tkinter as tk
from tkinter import messagebox
import requests
import re
from flask import Flask, request
import json


class AddPlayerPopup(tk.Frame):
    """ Popup Frame to Add a Phone """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        # Inputs
        tk.Label(self, text="Player Level:").grid(row=1, column=1)
        self._player_level = tk.Entry(self)
        self._player_level.grid(row=1, column=2)
        tk.Label(self, text="Job:").grid(row=2, column=1)
        self._job = tk.Entry(self)
        self._job.grid(row=2, column=2)

        # Submit / Close
        tk.Button(self, text="Submit", command=self._submit_cb).grid(
            row=9, column=1)
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=9, column=2)

    def _submit_cb(self):
        """ Submit the Add Player """

        # Validate the non-string data values
        if self._player_level.get() == "":
            messagebox.showerror(
                "Error", "Player level must be a valid integer")
            return

        # Create the dictionary for the JSON request body
        """ Adds a character to the backend server"""
        data = {}
        data['player_level'] = int(self._player_level.get())
        data['job'] = self._job.get()
        data['type'] = "player"

        headers = {"content-type": "application/json"}
        response = requests.post(
            "http://127.0.0.1:5000/server/characters", json=data, headers=headers)

        if response.status_code == 200:
            self._close_cb()
        else:
            messagebox.showerror(
                "Error", "Add Player Request Failed: " + response.text)
