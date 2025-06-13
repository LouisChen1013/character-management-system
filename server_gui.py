import re
import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import showinfo
import requests
from GUI.add_monster_popup import AddMonsterPopup
from GUI.add_player_popup import AddPlayerPopup
from GUI.player_update_popup import PlayerUpdatePopup
from GUI.monster_update_popup import MonsterUpdatePopup


def extract_character_id_from_selection(listbox):
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "No character selected.")
        return None, None

    entry = listbox.get(selected[0])
    match = re.search(r"id:\s*(\d+)", entry)
    if match:
        return match.group(1), entry
    else:
        messagebox.showerror("Error", "Unable to parse ID from selected entry.")
        return None, None


class MainAppController(tk.Frame):
    """Main Application for GUI"""

    def __init__(self, parent):
        super().__init__(parent)
        self._init_variables()
        self._init_widgets()
        self._refresh_all()

    def _init_variables(self):
        self._total_num_characters = tk.IntVar()
        self._num_monsters = tk.IntVar()
        self._num_players = tk.IntVar()
        self._avg_player_level = tk.IntVar()
        self._avg_monster_ai_difficulty = tk.StringVar()

    def _init_widgets(self):
        tk.Label(self, text="Characters in the Server").grid(
            row=1, column=2, padx=5, pady=5
        )

        self._characters_listbox = tk.Listbox(self, width=100)
        self._characters_listbox.grid(row=2, column=1, columnspan=5, padx=5, pady=5)

        button_data = [
            ("Show All Character", self._refresh_all, 1, 3, 1, "black"),
            ("Show Player", self._toggle_player, 2, 3, 1, "black"),
            ("Show Monster", self._toggle_monster, 3, 3, 1, "black"),
            ("Show Details", self._show_details, 4, 3, 1, "black"),
            ("Add Player", self._add_player, 1, 4, 1, "black"),
            ("Add Monster", self._add_monster, 2, 4, 1, "black"),
            ("Update Character", self._update_character, 3, 4, 1, "black"),
            ("Delete Character", self._delete_character, 4, 4, 1, "black"),
            ("Quit", self.quit, 2, 5, 2, "red"),
        ]

        for label, cmd, col, row, colspan, fg in button_data:
            tk.Button(self, text=label, command=cmd, fg=fg).grid(
                row=row, column=col, columnspan=colspan, padx=5, pady=5
            )

        self._build_stats_labels()

    def _build_stats_labels(self):
        stats_data = [
            ("Total Character:", self._total_num_characters, 6),
            ("Total Monsters:", self._num_monsters, 7),
            ("Total Players:", self._num_players, 8),
            ("Average Player Level:", self._avg_player_level, 9),
            ("Average Monster AI Difficulty:", self._avg_monster_ai_difficulty, 10),
        ]
        for label, var, row in stats_data:
            tk.Label(self, text=label).grid(
                row=row, column=2, padx=5, pady=2, sticky="w"
            )
            tk.Label(self, textvariable=var).grid(
                row=row, column=3, padx=5, pady=2, sticky="w"
            )

    def _refresh_all(self):
        self._update_characters_list()
        self._server_stats()

    def _safe_request(self, method, url, **kwargs):
        try:
            response = requests.request(method, url, timeout=5, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")
            return None

    def _add_player(self):
        self._popup_win = tk.Toplevel()
        AddPlayerPopup(self._popup_win, self._close_popup_cb)

    def _add_monster(self):
        self._popup_win = tk.Toplevel()
        AddMonsterPopup(self._popup_win, self._close_popup_cb)

    def _close_popup_cb(self):
        self._popup_win.destroy()
        self._refresh_all()

    def _update_character(self):
        char_id, entry = extract_character_id_from_selection(self._characters_listbox)
        if not char_id:
            return

        try:
            char_id = int(char_id)
            parts = entry.split()
            if "player" in entry:
                level = int(next(p for p in parts if p.isdigit()))
                job_type = parts[-1]
                self._popup_win = tk.Toplevel()
                PlayerUpdatePopup(
                    self._popup_win, char_id, level, job_type, self._close_popup_cb
                )
            else:
                difficulty = parts[-2]
                job_type = parts[-1]
                self._popup_win = tk.Toplevel()
                MonsterUpdatePopup(
                    self._popup_win, char_id, difficulty, job_type, self._close_popup_cb
                )
        except Exception:
            messagebox.showerror("Error", "Unable to parse character data.")

    def _show_details(self):
        char_id, _ = extract_character_id_from_selection(self._characters_listbox)
        if not char_id:
            return

        response = self._safe_request(
            "GET", f"http://127.0.0.1:5001/server/characters/details/{char_id}"
        )
        if response:
            showinfo("Character Stats", response.json())

    def _delete_character(self):
        char_id, _ = extract_character_id_from_selection(self._characters_listbox)
        if not char_id:
            return

        if messagebox.askyesno(
            "Confirm", "Are you sure you want to delete the character?"
        ):
            self._safe_request(
                "DELETE", f"http://127.0.0.1:5001/server/characters/{char_id}"
            )
            self._refresh_all()

    def _toggle_player(self):
        self._characters_listbox.delete(0, tk.END)
        response = self._safe_request(
            "GET", "http://127.0.0.1:5001/server/characters/all/player"
        )
        if response:
            for player in response.json():
                self._characters_listbox.insert(tk.END, player)

    def _toggle_monster(self):
        self._characters_listbox.delete(0, tk.END)
        response = self._safe_request(
            "GET", "http://127.0.0.1:5001/server/characters/all/monster"
        )
        if response:
            for monster in response.json():
                self._characters_listbox.insert(tk.END, monster)

    def _update_characters_list(self):
        self._characters_listbox.delete(0, tk.END)
        response = self._safe_request(
            "GET", "http://127.0.0.1:5001/server/characters/all_details"
        )
        if response:
            for character in response.json():
                self._characters_listbox.insert(tk.END, character)

    def _server_stats(self):
        response = self._safe_request("GET", "http://127.0.0.1:5001/server/serverstats")
        if response:
            stats = response.json()
            self._total_num_characters.set(stats.get("total_num_characters", 0))
            self._num_monsters.set(stats.get("num_monsters", 0))
            self._num_players.set(stats.get("num_players", 0))
            self._avg_player_level.set(stats.get("avg_player_level", 0))
            self._avg_monster_ai_difficulty.set(
                stats.get("avg_monster_ai_difficulty", "N/A")
            )


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Character Management System")
    root.geometry("900x500")
    MainAppController(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()
