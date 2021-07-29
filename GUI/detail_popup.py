import tkinter as tk
from tkinter import messagebox
import requests
import re


class DetailPopup(tk.Frame):
    """ Popup Frame to Update Character """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)

        from server_gui import MainAppController
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)
        tk.Label(self, textvariable=MainAppController).grid(
            row=6, column=3)
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=5, column=2)
