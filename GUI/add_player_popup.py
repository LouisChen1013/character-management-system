import tkinter as tk
from tkinter import messagebox
import requests


class AddPlayerPopup(tk.Frame):
    """Popup Frame to Add a Player"""

    def __init__(self, parent, close_callback):
        super().__init__(parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2, padx=10, pady=10)

        # Input Fields
        tk.Label(self, text="Player Level:").grid(
            row=1, column=1, sticky="e", padx=5, pady=5
        )
        self._player_level = tk.Entry(self)
        self._player_level.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(self, text="Job:").grid(row=2, column=1, sticky="e", padx=5, pady=5)
        self._job = tk.Entry(self)
        self._job.grid(row=2, column=2, padx=5, pady=5)

        # Buttons
        tk.Button(self, text="Submit", command=self._submit_cb).grid(
            row=4, column=1, pady=10
        )
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=4, column=2, pady=10
        )

    def _submit_cb(self):
        level = self._player_level.get().strip()
        job = self._job.get().strip()

        # Validate input
        if not level.isdigit():
            return messagebox.showerror(
                "Input Error", "Player level must be a valid integer."
            )
        if not job:
            return messagebox.showerror("Input Error", "Job cannot be empty.")

        data = {"player_level": int(level), "job": job, "type": "player"}

        headers = {"content-type": "application/json"}
        try:
            response = requests.post(
                "http://127.0.0.1:5001/server/characters",
                json=data,
                headers=headers,
                timeout=5,
            )
            response.raise_for_status()
            self._close_cb()
        except requests.HTTPError:
            try:
                error_msg = response.json().get("message", response.text)
            except Exception:
                error_msg = response.text or "Unknown error"
            messagebox.showerror("Error", f"Add Player Request Failed:\n{error_msg}")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Request Failed:\n{e}")
