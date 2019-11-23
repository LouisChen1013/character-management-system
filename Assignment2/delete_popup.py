import tkinter as tk
from tkinter import messagebox
import requests
import re
from flask import Flask, request
import json


class RemoveCharacterPopup(tk.Frame):
    """ Popup Frame to remove a character """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        tk.Label(self, text="ID:").grid(row=1, column=1)
        self.id = tk.Entry(self)
        self.id.grid(row=1, column=2)

        tk.Button(self, text="Submit", command=self._submit_cb).grid(
            row=9, column=1)
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=9, column=2)

    def _submit_cb(self):
        """ Submit the Remove Device """

        # Create the dictionary for the JSON request body
        data = {}
        data['id'] = self.id.get()

        # Implement your code here
        url = "http://127.0.0.1:5000/server/characters/" + data['id']
        response = requests.delete(url, json=data, headers={
                                   'Content-type': 'application/json'})

        if response.status_code == 200:
            self._close_cb()
