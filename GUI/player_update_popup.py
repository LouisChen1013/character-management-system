import tkinter as tk
from tkinter import messagebox
import requests


class PlayerUpdatePopup(tk.Frame):
    """Popup Frame to Update a Character"""

    def __init__(self, parent, selected_id, level, job, close_callback):
        super().__init__(parent)
        self._close_cb = close_callback
        self._selected_id = selected_id
        self.grid(rowspan=2, columnspan=2, padx=10, pady=10)

        tk.Label(self, text="ID:").grid(row=1, column=1, sticky="e", padx=5, pady=5)
        tk.Label(self, text=selected_id).grid(
            row=1, column=2, sticky="w", padx=5, pady=5
        )

        tk.Label(self, text="Level:").grid(row=2, column=1, sticky="e", padx=5, pady=5)
        self._player_level = tk.Entry(self)
        self._player_level.grid(row=2, column=2, padx=5, pady=5)

        tk.Label(self, text="Job:").grid(row=3, column=1, sticky="e", padx=5, pady=5)
        self._job = tk.Entry(self)
        self._job.grid(row=3, column=2, padx=5, pady=5)

        self._player_level.insert(0, level)
        self._job.insert(0, job)

        tk.Button(self, text="Submit", command=self._submit_cb).grid(
            row=5, column=1, padx=5, pady=10
        )
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=5, column=2, padx=5, pady=10
        )

    def _submit_cb(self):
        level = self._player_level.get().strip()
        job = self._job.get().strip()

        if not level.isdigit() or not job:
            return messagebox.showwarning(
                "Input Error",
                "Player level must be a number and job must not be empty.",
            )

        data = {"player_level": int(level), "job": job}

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
