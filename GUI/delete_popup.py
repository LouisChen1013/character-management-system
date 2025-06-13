import tkinter as tk
from tkinter import messagebox
import requests


class DeleteCharacterPopup(tk.Frame):
    """Popup Frame to Delete a Character by ID"""

    def __init__(self, parent, close_callback):
        super().__init__(parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2, padx=10, pady=10)

        tk.Label(self, text="Character ID:").grid(
            row=1, column=1, sticky="e", padx=5, pady=5
        )
        self._id_entry = tk.Entry(self)
        self._id_entry.grid(row=1, column=2, padx=5, pady=5)

        tk.Button(self, text="Submit", command=self._submit_cb).grid(
            row=3, column=1, padx=5, pady=10
        )
        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=3, column=2, padx=5, pady=10
        )

    def _submit_cb(self):
        char_id = self._id_entry.get().strip()

        if not char_id:
            return messagebox.showwarning(
                "Input Error", "Character ID cannot be empty."
            )
        if not char_id.isdigit():
            return messagebox.showwarning(
                "Input Error", "Character ID must be a number."
            )

        url = f"http://127.0.0.1:5001/server/characters/{char_id}"
        try:
            response = requests.delete(url, timeout=5)
            response.raise_for_status()
            self._close_cb()
        except requests.HTTPError:
            try:
                error_msg = response.json().get("message", response.text)
            except Exception:
                error_msg = response.text or "Unknown error"
            messagebox.showerror("Error", f"Delete failed:\n{error_msg}")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Request Error:\n{e}")
