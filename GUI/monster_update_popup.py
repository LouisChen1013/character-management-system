import tkinter as tk
from tkinter import messagebox
import requests


class MonsterUpdatePopup(tk.Frame):
    """Popup Frame to Update Monster Character"""

    def __init__(self, parent, selected_id, difficulty, monster_type, close_callback):
        super().__init__(parent)
        self._close_cb = close_callback
        self._selected_id = selected_id
        self.grid(rowspan=2, columnspan=2, padx=10, pady=10)

        tk.Label(self, text="ID:").grid(row=1, column=1, sticky="e", padx=5, pady=5)
        tk.Label(self, text=selected_id).grid(
            row=1, column=2, sticky="w", padx=5, pady=5
        )

        tk.Label(self, text="Monster Type:").grid(
            row=2, column=1, sticky="e", padx=5, pady=5
        )
        self._monster_type = tk.Entry(self)
        self._monster_type.grid(row=2, column=2, padx=5, pady=5)

        tk.Label(self, text="Monster AI Difficulty:").grid(
            row=3, column=1, sticky="e", padx=5, pady=5
        )
        self._monster_ai_difficulty = tk.Entry(self)
        self._monster_ai_difficulty.grid(row=3, column=2, padx=5, pady=5)

        self._monster_type.insert(0, monster_type)
        self._monster_ai_difficulty.insert(0, difficulty)

        tk.Button(self, text="Submit", command=self._submit_cb).grid(
            row=5, column=1, padx=5, pady=10
        )
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=5, column=2, padx=5, pady=10
        )

    def _submit_cb(self):
        monster_type = self._monster_type.get().strip()
        difficulty = self._monster_ai_difficulty.get().strip()

        if not monster_type or not difficulty:
            return messagebox.showwarning("Input Error", "All fields must be filled.")

        data = {"monster_type": monster_type, "monster_ai_difficulty": difficulty}

        headers = {"content-type": "application/json"}
        try:
            response = requests.put(
                f"http://127.0.0.1:5001/server/character/{self._selected_id}",
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
            messagebox.showerror("Error", f"Update failed:\n{error_msg}")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Request Error:\n{e}")
