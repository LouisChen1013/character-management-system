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
        self.player_level = tk.Entry(self)
        self.player_level.grid(row=1, column=2)
        tk.Label(self, text="Job:").grid(row=2, column=1)
        self.job = tk.Entry(self)
        self.job.grid(row=2, column=2)

        # Submit / Close
        tk.Button(self, text="Submit", command=self._submit_cb).grid(
            row=9, column=1)
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=9, column=2)

    def _submit_cb(self):
        """ Submit the Add Player """

        # # Validate the non-string data values
        # if re.match("^\d{4}-\d{2}-\d{2}$", self._received_date.get()) is None:
        #     messagebox.showerror(
        #         "Error", "Received date must have format yyyy-mm-dd")
        #     return

        # if re.match("^\d+$", self._storage_gb.get()) is None:
        #     messagebox.showerror("Error", "Storage must be a valid integer")
        #     return

        # if re.match("^\d+.\d{2}$", self._repair_price.get()) is None:
        #     messagebox.showerror("Error", "Repair Price must be a valid price")
        #     return

        # Create the dictionary for the JSON request body
        data = {}
        data['player_level'] = self.player_level.get()
        data['job'] = self.job.get()
        data['type'] = "player"

        # Implement your code here
        url = "http://127.0.0.1:5000/server/character"
        response = requests.post(url, json=data, headers={
                                 'Content-type': 'application/json'})

        if response.status_code == 200:
            self._close_cb()
