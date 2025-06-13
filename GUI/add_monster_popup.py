import tkinter as tk
from tkinter import messagebox
import requests


class AddMonsterPopup(tk.Frame):
    """Popup Frame to Add a Monster"""

    def __init__(self, parent, close_callback):
        super().__init__(parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2, padx=10, pady=10)

        # Monster Type
        tk.Label(self, text="Monster Type:").grid(
            row=1, column=1, sticky="e", padx=5, pady=5
        )
        self._monster_type = tk.Entry(self)
        self._monster_type.grid(row=1, column=2, padx=5, pady=5)

        # Monster AI Difficulty
        tk.Label(self, text="Monster AI Difficulty:").grid(
            row=2, column=1, sticky="e", padx=5, pady=5
        )
        self._monster_ai_difficulty = tk.Entry(self)
        self._monster_ai_difficulty.grid(row=2, column=2, padx=5, pady=5)

        # Buttons
        tk.Button(self, text="Submit", command=self._submit_cb).grid(
            row=4, column=1, padx=5, pady=10
        )
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=4, column=2, padx=5, pady=10
        )

    def _submit_cb(self):
        """Submit the Add Monster"""

        monster_type = self._monster_type.get().strip()
        difficulty = self._monster_ai_difficulty.get().strip()

        if not monster_type or not difficulty:
            return messagebox.showwarning("Input Error", "All fields must be filled.")

        data = {
            "monster_type": monster_type,
            "monster_ai_difficulty": difficulty,
            "type": "monster",
        }

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
