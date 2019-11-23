import tkinter as tk
from tkinter import messagebox
import requests
import re


class CompletePopup(tk.Frame):
    """ Popup Frame to Complete a Repair """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        tk.Label(self, text="Serial Num:").grid(row=1, column=1)
        self._serial_num = tk.Entry(self)
        self._serial_num.grid(row=1, column=2)
        tk.Label(self, text="Repair Cost:").grid(row=2, column=1)
        self._cost = tk.Entry(self)
        self._cost.grid(row=2, column=2)
        tk.Button(self, text="Submit", command=self._submit_cb).grid(
            row=7, column=1)
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=7, column=2)

    def _submit_cb(self):
        """ Submit Complete Repair """

        if re.match("^\d+.\d{2}$", self._cost.get()) is None:
            messagebox.showerror("Error", "Repair Cost must be a valid price")
            return

        data = {}
        data['serial_num'] = self._serial_num.get()
        data['cost'] = float(self._cost.get())

        headers = {"content-type": "application/json"}
        response = requests.put(
            "http://127.0.0.1:5000/repairshop/devices/complete", json=data, headers=headers)

        if response.status_code == 200:
            self._close_cb()
        else:
            messagebox.showerror(
                "Error", "Cannot update point because: " + response.text)
