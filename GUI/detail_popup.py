import tkinter as tk


class DetailPopup(tk.Frame):
    """Popup Frame to show Character Details"""

    def __init__(self, parent, text_data, close_callback):
        super().__init__(parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2, padx=10, pady=10)

        tk.Label(self, text="Character Details:").grid(
            row=1, column=1, sticky="w", padx=5, pady=5
        )
        self._text = tk.Text(self, height=10, width=50)
        self._text.insert(tk.END, text_data)
        self._text.config(state=tk.DISABLED)
        self._text.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        tk.Button(self, text="Close", command=self._close_cb).grid(
            row=3, column=2, padx=5, pady=10
        )
