"""
Multiplayer Daily Activity Tracker - Beautiful Edition
A competitive multiplayer GUI application with modern design
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import uuid
from pathlib import Path

# Colors - Modern gradient theme
COLORS = {
    "bg_dark": "#0D1117",
    "bg_light": "#161B22",
    "bg_lighter": "#21262D",
    "bg_darker": "#010409",
    "accent_blue": "#58A6FF",
    "accent_green": "#3FB950",
    "accent_red": "#F85149",
    "accent_yellow": "#D29922",
    "text_primary": "#C9D1D9",
    "text_secondary": "#8B949E",
    "border": "#30363D",
}


# Data paths
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "multiplayer_data")
os.makedirs(DATA_DIR, exist_ok=True)

PLAYERS_FILE = os.path.join(DATA_DIR, "players.json")


class Task:
    """Represents a trackable task"""
    def __init__(self, name, points, is_positive=True, task_id=None):
        self.id = task_id or str(uuid.uuid4())[:8]
        self.name = name
        self.points = points
        self.is_positive = is_positive

    def to_dict(self):
        return {"id": self.id, "name": self.name, "points": self.points, "is_positive": self.is_positive}

    @staticmethod
    def from_dict(data):
        return Task(data["name"], data["points"], data.get("is_positive", True), data.get("id"))




class Player:
    """Represents a player"""
    def __init__(self, name, player_id=None):
        self.id = player_id or str(uuid.uuid4())[:8]
        self.name = name
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {"id": self.id, "name": self.name, "created_at": self.created_at}

    @staticmethod
    def from_dict(data):
        p = Player(data["name"], data["id"])
        p.created_at = data.get("created_at", datetime.now().isoformat())
        return p

    def get_tasks_file(self):
        return os.path.join(DATA_DIR, f"{self.id}_tasks.json")

    def get_logs_file(self):
        return os.path.join(DATA_DIR, f"{self.id}_logs.json")


class DataManager:
    """Handles data persistence"""

    @staticmethod
    def load_players():
        if os.path.exists(PLAYERS_FILE):
            try:
                with open(PLAYERS_FILE, 'r') as f:
                    return [Player.from_dict(p) for p in json.load(f)]
            except:
                pass
        return []

    @staticmethod
    def save_players(players):
        with open(PLAYERS_FILE, 'w') as f:
            json.dump([p.to_dict() for p in players], f, indent=2)

    @staticmethod
    def load_tasks(player):
        try:
            with open(player.get_tasks_file(), 'r') as f:
                return [Task.from_dict(t) for t in json.load(f)]
        except:
            return [
                Task("Morning Exercise", 15, True),
                Task("Study/Work", 20, True),
                Task("Reading", 10, True),
                Task("Meditation", 5, True),
                Task("Good Meal", 5, True),
                Task("Sleep 8hrs", 10, True),
                Task("Skipped Workout", -15, False),
                Task("Junk Food", -10, False),
            ]

    @staticmethod
    def save_tasks(player, tasks):
        with open(player.get_tasks_file(), 'w') as f:
            json.dump([t.to_dict() for t in tasks], f, indent=2)

    @staticmethod
    def load_logs(player):
        try:
            with open(player.get_logs_file(), 'r') as f:
                return json.load(f)
        except:
            return {}

    @staticmethod
    def save_logs(player, logs):
        with open(player.get_logs_file(), 'w') as f:
            json.dump(logs, f, indent=2)




class TaskCard(tk.Frame):
    """Beautiful task card widget"""
    def __init__(self, parent, task, is_completed, on_toggle, editable=True):
        super().__init__(parent, bg=COLORS["bg_lighter"], relief="flat", height=60)
        self.pack_propagate(False)
        self.task = task
        self.is_completed = is_completed
        self.on_toggle = on_toggle
        self.editable = editable
        
        # Left side - checkbox and name
        left = tk.Frame(self, bg=COLORS["bg_lighter"])
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Checkbox
        checkbox_text = "✓" if is_completed else "○"
        checkbox_color = COLORS["accent_green"] if is_completed else COLORS["text_secondary"]
        
        self.checkbox = tk.Label(
            left, text=checkbox_text, font=("Arial", 16, "bold"),
            fg=checkbox_color, bg=COLORS["bg_lighter"]
        )
        self.checkbox.pack(side=tk.LEFT, padx=(0, 12))
        
        # Task name
        name_color = COLORS["accent_green"] if is_completed else COLORS["text_primary"]
        self.name_label = tk.Label(
            left, text=task.name, font=("Segoe UI", 11),
            fg=name_color, bg=COLORS["bg_lighter"]
        )
        self.name_label.pack(side=tk.LEFT)
        
        # Right side - points
        right = tk.Frame(self, bg=COLORS["bg_lighter"])
        right.pack(side=tk.RIGHT, padx=15, pady=10)
        
        points_color = COLORS["accent_green"] if task.is_positive else COLORS["accent_red"]
        points_text = f"{'+ ' if task.points > 0 else ''}{task.points} pts"
        
        tk.Label(
            right, text=points_text, font=("Segoe UI", 11, "bold"),
            fg=points_color, bg=COLORS["bg_lighter"]
        ).pack()
        
        if editable:
            self.bind("<Button-1>", self._on_click)
            left.bind("<Button-1>", self._on_click)
            self.checkbox.bind("<Button-1>", self._on_click)
            self.name_label.bind("<Button-1>", self._on_click)
            right.bind("<Button-1>", self._on_click)
    
    def _on_click(self, e):
        if self.editable:
            self.on_toggle(self.task.id)


class ScoreBoard(tk.Frame):
    """Beautiful scoreboard display"""
    def __init__(self, parent, player1_name, player1_score, player2_name, player2_score):
        super().__init__(parent, bg=COLORS["bg_light"], relief="flat", height=100)
        self.pack_propagate(False)
        
        # Determine winner
        winner = None
        if player1_score > player2_score:
            winner = 1
        elif player2_score > player1_score:
            winner = 2
        
        # Left player
        left_frame = tk.Frame(self, bg=COLORS["bg_light"])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        p1_color = COLORS["accent_yellow"] if winner == 1 else COLORS["text_secondary"]
        tk.Label(left_frame, text=player1_name.upper(), font=("Segoe UI", 10, "bold"),
                fg=p1_color, bg=COLORS["bg_light"]).pack()
        tk.Label(left_frame, text=str(player1_score), font=("Segoe UI", 28, "bold"),
                fg=COLORS["accent_blue"], bg=COLORS["bg_light"]).pack()
        
        # VS
        tk.Label(self, text="VS", font=("Segoe UI", 12, "bold"),
                fg=COLORS["text_secondary"], bg=COLORS["bg_light"]).pack(side=tk.LEFT, padx=20)
        
        # Right player
        right_frame = tk.Frame(self, bg=COLORS["bg_light"])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        p2_color = COLORS["accent_yellow"] if winner == 2 else COLORS["text_secondary"]
        tk.Label(right_frame, text=player2_name.upper(), font=("Segoe UI", 10, "bold"),
                fg=p2_color, bg=COLORS["bg_light"]).pack()
        tk.Label(right_frame, text=str(player2_score), font=("Segoe UI", 28, "bold"),
                fg=COLORS["accent_blue"], bg=COLORS["bg_light"]).pack()


class MultiplayerApp:
    """Main application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Multiplayer Daily Tracker")
        self.root.geometry("1600x900")
        self.root.minsize(1200, 700)
        self.root.configure(bg=COLORS["bg_dark"])
        
        self.all_players = DataManager.load_players()
        self.current_player = None
        self.rival_player = None
        
        self.show_welcome()
    
    def show_welcome(self):
        """Welcome screen with player selection"""
        self.clear_window()
        
        # Title
        title = tk.Label(
            self.root, text="⚔ MULTIPLAYER TRACKER",
            font=("Segoe UI", 32, "bold"), fg=COLORS["accent_blue"],
            bg=COLORS["bg_dark"]
        )
        title.pack(pady=40)
        
        subtitle = tk.Label(
            self.root, text="Compete with your friend and track your progress",
            font=("Segoe UI", 12), fg=COLORS["text_secondary"],
            bg=COLORS["bg_dark"]
        )
        subtitle.pack(pady=10)
        
        # Player selection frame
        players_frame = tk.Frame(self.root, bg=COLORS["bg_dark"])
        players_frame.pack(pady=30, expand=True)
        
        tk.Label(
            players_frame, text="Select Your Profile:",
            font=("Segoe UI", 14, "bold"), fg=COLORS["text_primary"],
            bg=COLORS["bg_dark"]
        ).pack(pady=10)
        
        # List existing players
        if self.all_players:
            for player in self.all_players:
                btn = tk.Button(
                    players_frame, text=f"👤 {player.name}",
                    font=("Segoe UI", 11), 
                    bg=COLORS["accent_blue"], fg="white",
                    relief="flat", padx=30, pady=10, bd=0,
                    command=lambda p=player: self.select_player(p)
                )
                btn.pack(pady=5)
        
        # New player
        tk.Label(
            players_frame, text="─" * 30,
            font=("Segoe UI", 10), fg=COLORS["border"],
            bg=COLORS["bg_dark"]
        ).pack(pady=10)
        
        tk.Label(
            players_frame, text="New Player:",
            font=("Segoe UI", 12, "bold"), fg=COLORS["text_primary"],
            bg=COLORS["bg_dark"]
        ).pack(pady=5)
        
        name_var = tk.StringVar()
        name_entry = tk.Entry(
            players_frame, textvariable=name_var,
            font=("Segoe UI", 11), bg=COLORS["bg_lighter"],
            fg=COLORS["text_primary"], insertbackground=COLORS["accent_blue"],
            relief="flat", bd=0, width=25
        )
        name_entry.pack(pady=10, padx=10)
        name_entry.focus()
        
        btn = tk.Button(
            players_frame, text="Create New Player",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["accent_green"], fg="white",
            relief="flat", padx=20, pady=10, bd=0,
            command=lambda: self.create_player(name_var.get())
        )
        btn.pack(pady=10)
    
    def select_player(self, player):
        """Select existing player"""
        self.current_player = player
        self.show_rival_selection()
    
    def create_player(self, name):
        """Create new player"""
        if not name.strip():
            messagebox.showwarning("Invalid", "Please enter a name")
            return
        
        if any(p.name.lower() == name.lower() for p in self.all_players):
            messagebox.showwarning("Duplicate", "Player already exists")
            return
        
        self.current_player = Player(name)
        self.all_players.append(self.current_player)
        DataManager.save_players(self.all_players)
        DataManager.save_tasks(self.current_player, DataManager.load_tasks(self.current_player))
        
        self.show_rival_selection()
    
    def show_rival_selection(self):
        """Select rival player"""
        rivals = [p for p in self.all_players if p.id != self.current_player.id]
        
        if not rivals:
            messagebox.showinfo("Info", "No rivals yet! Have your friend create an account.")
            self.show_welcome()
            return
        
        self.clear_window()
        
        # Title
        tk.Label(
            self.root, text=f"Welcome, {self.current_player.name}! 🎮",
            font=("Segoe UI", 24, "bold"), fg=COLORS["accent_blue"],
            bg=COLORS["bg_dark"]
        ).pack(pady=30)
        
        tk.Label(
            self.root, text="Choose your rival:",
            font=("Segoe UI", 12), fg=COLORS["text_secondary"],
            bg=COLORS["bg_dark"]
        ).pack(pady=10)
        
        # Rival buttons
        rivals_frame = tk.Frame(self.root, bg=COLORS["bg_dark"])
        rivals_frame.pack(pady=30, expand=True)
        
        for rival in rivals:
            btn = tk.Button(
                rivals_frame, text=f"⚔ Battle {rival.name}",
                font=("Segoe UI", 12, "bold"),
                bg=COLORS["accent_red"], fg="white",
                relief="flat", padx=40, pady=15, bd=0,
                command=lambda r=rival: self.start_game(r)
            )
            btn.pack(pady=10)
        
        # Back button
        btn = tk.Button(
            rivals_frame, text="← Back",
            font=("Segoe UI", 10),
            bg=COLORS["bg_lighter"], fg=COLORS["text_secondary"],
            relief="flat", padx=20, pady=8, bd=0,
            command=self.show_welcome
        )
        btn.pack(pady=20)
    
    def start_game(self, rival):
        """Start the game"""
        self.rival_player = rival
        self.load_game_data()
        self.show_game()
    
    def load_game_data(self):
        """Load player data"""
        self.today = datetime.now().strftime("%Y-%m-%d")
        
        self.current_tasks = DataManager.load_tasks(self.current_player)
        self.current_logs = DataManager.load_logs(self.current_player)
        
        self.rival_tasks = DataManager.load_tasks(self.rival_player)
        self.rival_logs = DataManager.load_logs(self.rival_player)
        
        # Get completed tasks for today
        if self.today in self.current_logs:
            self.current_completed = set(self.current_logs[self.today].get("tasks", []))
        else:
            self.current_completed = set()
        
        if self.today in self.rival_logs:
            self.rival_completed = set(self.rival_logs[self.today].get("tasks", []))
        else:
            self.rival_completed = set()
    
    def get_score(self, tasks, completed):
        """Calculate score from tasks"""
        return sum(t.points for t in tasks if t.id in completed)
    
    def show_game(self):
        """Main game screen"""
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg=COLORS["bg_light"], height=70)
        header.pack(fill=tk.X, pady=0)
        header.pack_propagate(False)
        
        tk.Label(
            header, text="⚔ DAILY BATTLE",
            font=("Segoe UI", 18, "bold"), fg=COLORS["accent_blue"],
            bg=COLORS["bg_light"]
        ).pack(pady=10)
        
        # Scoreboard
        current_score = self.get_score(self.current_tasks, self.current_completed)
        rival_score = self.get_score(self.rival_tasks, self.rival_completed)
        
        ScoreBoard(
            header, self.current_player.name, current_score,
            self.rival_player.name, rival_score
        ).pack(fill=tk.X, padx=20, pady=5)
        
        # Main content
        content = tk.Frame(self.root, bg=COLORS["bg_dark"])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side - Current player
        left_panel = tk.Frame(content, bg=COLORS["bg_dark"])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(
            left_panel, text=f"📋 {self.current_player.name}'s Tasks",
            font=("Segoe UI", 12, "bold"), fg=COLORS["accent_green"],
            bg=COLORS["bg_dark"]
        ).pack(pady=10)
        
        current_scroll = tk.Canvas(left_panel, bg=COLORS["bg_darker"], highlightthickness=0)
        current_scroll.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = tk.Scrollbar(left_panel, orient=tk.VERTICAL, command=current_scroll.yview,
                                bg=COLORS["bg_dark"], troughcolor=COLORS["bg_lighter"])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        current_scroll.configure(yscrollcommand=scrollbar.set)
        current_frame = tk.Frame(current_scroll, bg=COLORS["bg_darker"])
        current_scroll.create_window((0, 0), window=current_frame, anchor=tk.NW)
        
        for task in self.current_tasks:
            is_done = task.id in self.current_completed
            TaskCard(
                current_frame, task, is_done,
                lambda tid: self.toggle_task("current", tid),
                editable=True
            ).pack(fill=tk.X, pady=3)
        
        current_frame.bind(
            "<Configure>",
            lambda e: current_scroll.configure(scrollregion=current_scroll.bbox("all"))
        )
        
        # Right side - Rival player
        right_panel = tk.Frame(content, bg=COLORS["bg_dark"])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(
            right_panel, text=f"📋 {self.rival_player.name}'s Tasks",
            font=("Segoe UI", 12, "bold"), fg=COLORS["accent_red"],
            bg=COLORS["bg_dark"]
        ).pack(pady=10)
        
        rival_scroll = tk.Canvas(right_panel, bg=COLORS["bg_darker"], highlightthickness=0)
        rival_scroll.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar2 = tk.Scrollbar(right_panel, orient=tk.VERTICAL, command=rival_scroll.yview,
                                 bg=COLORS["bg_dark"], troughcolor=COLORS["bg_lighter"])
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        
        rival_scroll.configure(yscrollcommand=scrollbar2.set)
        rival_frame = tk.Frame(rival_scroll, bg=COLORS["bg_darker"])
        rival_scroll.create_window((0, 0), window=rival_frame, anchor=tk.NW)
        
        for task in self.rival_tasks:
            is_done = task.id in self.rival_completed
            TaskCard(rival_frame, task, is_done, lambda tid: None, editable=False).pack(fill=tk.X, pady=3)
        
        rival_frame.bind(
            "<Configure>",
            lambda e: rival_scroll.configure(scrollregion=rival_scroll.bbox("all"))
        )
        
        # Footer
        footer = tk.Frame(self.root, bg=COLORS["bg_light"], height=60)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        btn = tk.Button(
            footer, text="← Back to Players",
            font=("Segoe UI", 10),
            bg=COLORS["bg_lighter"], fg=COLORS["text_secondary"],
            relief="flat", padx=20, pady=8, bd=0,
            command=self.show_rival_selection
        )
        btn.pack(side=tk.LEFT, padx=20, pady=10)
    
    def toggle_task(self, player, task_id):
        """Toggle task completion"""
        if player == "current":
            if task_id in self.current_completed:
                self.current_completed.remove(task_id)
            else:
                self.current_completed.add(task_id)
            
            # Save
            if self.today not in self.current_logs:
                self.current_logs[self.today] = {}
            self.current_logs[self.today]["tasks"] = list(self.current_completed)
            DataManager.save_logs(self.current_player, self.current_logs)
            
            self.show_game()
    
    def clear_window(self):
        """Clear all widgets"""
        for widget in self.root.winfo_children():
            widget.destroy()


def main():
    root = tk.Tk()
    app = MultiplayerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

    BG_SECONDARY = "#1a1a1a"
    FG_COLOR = "#00ff00"
    FG_ACCENT = "#00cc00"
    POSITIVE_COLOR = "#00ff00"
    NEGATIVE_COLOR = "#ff4444"
    
    def __init__(self, parent, existing_players):
        super().__init__(parent)
        self.title("Player Setup")
        self.geometry("400x350")
        self.configure(bg=self.BG_COLOR)
        self.transient(parent)
        self.grab_set()
        self.selected_player = None
        self.new_player = None
        
        self.existing_players = existing_players
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        tk.Label(self, text="🎮 Select or Create Player", bg=self.BG_COLOR, fg=self.FG_COLOR,
                font=("Menlo", 14, "bold")).pack(pady=20)
        
        # Existing players
        if self.existing_players:
            tk.Label(self, text="Existing Players:", bg=self.BG_COLOR, fg=self.FG_ACCENT,
                    font=("Menlo", 11, "bold")).pack(anchor=tk.W, padx=30, pady=(10, 5))
            
            self.selected = tk.StringVar()
            for player in self.existing_players:
                btn = tk.Radiobutton(self, text=f"  {player.name}", variable=self.selected,
                                    value=player.id, bg=self.BG_COLOR, fg=self.FG_COLOR,
                                    selectcolor=self.BG_SECONDARY, font=("Menlo", 11))
                btn.pack(anchor=tk.W, padx=40)
            
            tk.Button(self, text="Select Player", bg=self.BG_SECONDARY, fg=self.FG_COLOR,
                     relief="flat", command=self.select_player).pack(pady=10)
        
        # Separator
        if self.existing_players:
            tk.Frame(self, bg=self.FG_ACCENT, height=1).pack(fill=tk.X, pady=15, padx=30)
        
        # New player
        tk.Label(self, text="Create New Player:", bg=self.BG_COLOR, fg=self.FG_ACCENT,
                font=("Menlo", 11, "bold")).pack(anchor=tk.W, padx=30, pady=(10, 5))
        
        tk.Label(self, text="Name:", bg=self.BG_COLOR, fg=self.FG_COLOR,
                font=("Menlo", 10)).pack(anchor=tk.W, padx=40)
        
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(self, textvariable=self.name_var,
                                   bg=self.BG_SECONDARY, fg=self.FG_COLOR,
                                   insertbackground=self.FG_COLOR, font=("Menlo", 10),
                                   relief="flat", bd=5, width=30)
        self.name_entry.pack(fill=tk.X, padx=40, pady=5)
        self.name_entry.focus()
        
        tk.Button(self, text="Create New Player", bg=self.BG_SECONDARY, fg=self.FG_COLOR,
                 relief="flat", command=self.create_player).pack(pady=10)
    
    def select_player(self):
        if hasattr(self, 'selected') and self.selected.get():
            player_id = self.selected.get()
            self.selected_player = next((p for p in self.existing_players if p.id == player_id), None)
            self.destroy()
        else:
            messagebox.showwarning("Select Player", "Please select a player")
    
    def create_player(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Invalid Name", "Please enter a player name")
            return
        
        if any(p.name.lower() == name.lower() for p in self.existing_players):
            messagebox.showwarning("Duplicate", "A player with this name already exists")
            return
        
        self.new_player = Player(name)
        self.destroy()


class MultiplayerTrackerApp:
    """Main multiplayer tracker application"""
    
    BG_COLOR = "#0a0a0a"
    BG_SECONDARY = "#1a1a1a"
    FG_COLOR = "#00ff00"
    FG_ACCENT = "#00cc00"
    FG_DIMMED = "#008800"
    POSITIVE_COLOR = "#00ff00"
    NEGATIVE_COLOR = "#ff4444"
    
    def __init__(self, root):
        self.root = root
        self.root.title("Multiplayer Daily Tracker")
        self.root.geometry("1800x950")
        self.root.minsize(1600, 850)
        self.root.configure(bg=self.BG_COLOR)
        
        # Load all players
        self.all_players = DataManager.load_players()
        self.current_player = None
        self.rival_player = None
        
        self.setup_styles()
        self.show_player_selection()
    
    def show_player_selection(self):
        """Show initial player selection/creation window"""
        window = PlayerSetupWindow(self.root, self.all_players)
        self.root.wait_window(window)
        
        if window.selected_player:
            self.current_player = window.selected_player
        elif window.new_player:
            self.current_player = window.new_player
            self.all_players.append(self.current_player)
            DataManager.save_players(self.all_players)
        else:
            self.root.destroy()
            return
        
        # Now select rival player
        self.show_rival_selection()
    
    def show_rival_selection(self):
        """Select a rival player to compete with"""
        rival_options = [p for p in self.all_players if p.id != self.current_player.id]
        
        if not rival_options:
            messagebox.showinfo("No Rivals", 
                "No rival players found. Invite a friend to create their account!")
            self.root.destroy()
            return
        
        window = tk.Toplevel(self.root)
        window.title("Select Your Rival")
        window.geometry("300x250")
        window.configure(bg=self.BG_COLOR)
        window.transient(self.root)
        window.grab_set()
        
        tk.Label(window, text=f"Hello {self.current_player.name}! 🎮\nWho do you want to compete with?",
                bg=self.BG_COLOR, fg=self.FG_COLOR, font=("Menlo", 11, "bold")).pack(pady=15)
        
        selected = tk.StringVar()
        for player in rival_options:
            tk.Radiobutton(window, text=f"  {player.name}", variable=selected,
                          value=player.id, bg=self.BG_COLOR, fg=self.FG_COLOR,
                          selectcolor=self.BG_SECONDARY, font=("Menlo", 10)).pack(anchor=tk.W, padx=30)
        
        def confirm():
            if selected.get():
                self.rival_player = next((p for p in rival_options if p.id == selected.get()), None)
                window.destroy()
                self.load_player_data()
                self.setup_ui()
        
        tk.Button(window, text="Start Competing", bg=self.BG_SECONDARY, fg=self.FG_COLOR,
                 relief="flat", command=confirm).pack(pady=15)
    
    def load_player_data(self):
        """Load all data for current and rival players"""
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.current_week = self.get_week_key(datetime.now())
        self.current_month = datetime.now().strftime("%Y-%m")
        
        # Current player data
        self.tasks = DataManager.load_tasks(self.current_player.id)
        self.logs = DataManager.load_logs(self.current_player.id)
        self.weekly_tasks = DataManager.load_weekly_tasks(self.current_player.id)
        self.weekly_logs = DataManager.load_weekly_logs(self.current_player.id)
        self.monthly_tasks = DataManager.load_monthly_tasks(self.current_player.id)
        self.monthly_logs = DataManager.load_monthly_logs(self.current_player.id)
        
        # Rival player data
        self.rival_tasks = DataManager.load_tasks(self.rival_player.id)
        self.rival_logs = DataManager.load_logs(self.rival_player.id)
        self.rival_weekly_tasks = DataManager.load_weekly_tasks(self.rival_player.id)
        self.rival_weekly_logs = DataManager.load_weekly_logs(self.rival_player.id)
        self.rival_monthly_tasks = DataManager.load_monthly_tasks(self.rival_player.id)
        self.rival_monthly_logs = DataManager.load_monthly_logs(self.rival_player.id)
        
        # Track completed tasks
        self.completed_selected = set()
        if self.today in self.logs:
            self.completed_selected = set(self.logs[self.today].get("completed_tasks", []))
        
        self.completed_weekly = set()
        if self.current_week in self.weekly_logs:
            self.completed_weekly = set(self.weekly_logs[self.current_week].get("completed_tasks", []))
        
        self.completed_monthly = set()
        if self.current_month in self.monthly_logs:
            self.completed_monthly = set(self.monthly_logs[self.current_month].get("completed_tasks", []))
        
        self.task_frames = {}
    
    def get_week_key(self, date):
        """Get a unique key for the week"""
        return f"{date.year}-W{date.isocalendar()[1]:02d}"
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TFrame', background=self.BG_COLOR)
    
    def setup_ui(self):
        """Setup main user interface"""
        # Header
        header = tk.Frame(self.root, bg=self.BG_SECONDARY, height=80)
        header.pack(fill=tk.X, padx=10, pady=10)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="⚔️  MULTIPLAYER TRACKER", 
                        bg=self.BG_SECONDARY, fg=self.POSITIVE_COLOR,
                        font=("Menlo", 18, "bold"))
        title.pack(pady=10)
        
        # Players info
        info_frame = tk.Frame(header, bg=self.BG_SECONDARY)
        info_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(info_frame, text=f"👤 {self.current_player.name}", 
                bg=self.BG_SECONDARY, fg=self.FG_COLOR,
                font=("Menlo", 12, "bold")).pack(side=tk.LEFT, padx=20)
        
        tk.Label(info_frame, text=" VS ", 
                bg=self.BG_SECONDARY, fg=self.FG_ACCENT,
                font=("Menlo", 12, "bold")).pack(side=tk.LEFT, padx=10)
        
        tk.Label(info_frame, text=f"👤 {self.rival_player.name}", 
                bg=self.BG_SECONDARY, fg=self.FG_COLOR,
                font=("Menlo", 12, "bold")).pack(side=tk.LEFT, padx=20)
        
        # Main content with tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Daily tab
        daily_frame = tk.Frame(notebook, bg=self.BG_COLOR)
        notebook.add(daily_frame, text="Daily")
        self.setup_daily_tab(daily_frame)
        
        # Leaderboard tab
        leaderboard_frame = tk.Frame(notebook, bg=self.BG_COLOR)
        notebook.add(leaderboard_frame, text="Leaderboard")
        self.setup_leaderboard_tab(leaderboard_frame)
        
        # Weekly tab
        weekly_frame = tk.Frame(notebook, bg=self.BG_COLOR)
        notebook.add(weekly_frame, text="Weekly")
        self.setup_weekly_tab(weekly_frame)
        
        # Monthly tab
        monthly_frame = tk.Frame(notebook, bg=self.BG_COLOR)
        notebook.add(monthly_frame, text="Monthly")
        self.setup_monthly_tab(monthly_frame)
    
    def setup_daily_tab(self, parent):
        """Setup daily tasks tab with split view (player vs rival)"""
        # Create split view containers
        left_frame = tk.Frame(parent, bg=self.BG_COLOR)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = tk.Frame(parent, bg=self.BG_COLOR)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Current player
        tk.Label(left_frame, text=f"📋 {self.current_player.name}'s Tasks", 
                bg=self.BG_COLOR, fg=self.FG_COLOR, font=("Menlo", 12, "bold")).pack(pady=10)
        
        left_scroll = tk.Canvas(left_frame, bg=self.BG_SECONDARY, highlightthickness=0)
        left_scroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        left_scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=left_scroll.yview)
        left_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        left_content = tk.Frame(left_scroll, bg=self.BG_SECONDARY)
        left_scroll.create_window((0, 0), window=left_content, anchor=tk.NW)
        left_scroll.configure(yscrollcommand=left_scrollbar.set)
        left_content.bind("<Configure>", lambda e: left_scroll.configure(scrollregion=left_scroll.bbox("all")))
        
        self.create_task_list(left_content, self.tasks, self.completed_selected, is_current_player=True)
        
        # Right side - Rival player
        tk.Label(right_frame, text=f"📋 {self.rival_player.name}'s Tasks", 
                bg=self.BG_COLOR, fg=self.FG_COLOR, font=("Menlo", 12, "bold")).pack(pady=10)
        
        right_scroll = tk.Canvas(right_frame, bg=self.BG_SECONDARY, highlightthickness=0)
        right_scroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_scrollbar = tk.Scrollbar(right_frame, orient=tk.VERTICAL, command=right_scroll.yview)
        right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        right_content = tk.Frame(right_scroll, bg=self.BG_SECONDARY)
        right_scroll.create_window((0, 0), window=right_content, anchor=tk.NW)
        right_scroll.configure(yscrollcommand=right_scrollbar.set)
        right_content.bind("<Configure>", lambda e: right_scroll.configure(scrollregion=right_scroll.bbox("all")))
        
        self.create_task_list(right_content, self.rival_tasks, set(), is_current_player=False)
        
        # Score display
        score_frame = tk.Frame(parent, bg=self.BG_SECONDARY, height=60)
        score_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)
        score_frame.pack_propagate(False)
        
        self.update_daily_scores(score_frame)
    
    def create_task_list(self, parent, tasks, completed, is_current_player=True):
        """Create task list for display"""
        for task in tasks:
            frame = tk.Frame(parent, bg=self.BG_COLOR, relief="raised", bd=1)
            frame.pack(fill=tk.X, pady=5, padx=5)
            
            inner = tk.Frame(frame, bg=self.BG_COLOR, padx=10, pady=8)
            inner.pack(fill=tk.BOTH, expand=True)
            
            # Task name and status
            task_completed = task.id in completed
            color = self.POSITIVE_COLOR if task.is_positive else self.NEGATIVE_COLOR
            status_icon = "✓" if task_completed else "○"
            
            name_label = tk.Label(inner, text=f"{status_icon} {task.name}", 
                                 bg=self.BG_COLOR, fg=color, font=("Menlo", 10))
            name_label.pack(side=tk.LEFT)
            
            points_label = tk.Label(inner, text=f"{'+' if task.points > 0 else ''}{task.points} pts",
                                   bg=self.BG_COLOR, fg=color, font=("Menlo", 9, "bold"))
            points_label.pack(side=tk.RIGHT)
            
            if is_current_player:
                def toggle_task(t=task):
                    if t.id in completed:
                        completed.remove(t.id)
                    else:
                        completed.add(t.id)
                    self.save_daily_progress()
                    self.refresh_ui()
                
                frame.bind("<Button-1>", lambda e: toggle_task())
                inner.bind("<Button-1>", lambda e: toggle_task())
                name_label.bind("<Button-1>", lambda e: toggle_task())
    
    def save_daily_progress(self):
        """Save current player's daily progress"""
        if self.today not in self.logs:
            self.logs[self.today] = {"completed_tasks": [], "total_points": 0}
        
        self.logs[self.today]["completed_tasks"] = list(self.completed_selected)
        
        # Calculate daily points
        total = sum(t.points for t in self.tasks if t.id in self.completed_selected)
        self.logs[self.today]["total_points"] = total
        self.logs[self.today]["timestamp"] = datetime.now().isoformat()
        
        DataManager.save_logs(self.current_player.id, self.logs)
    
    def update_daily_scores(self, parent):
        """Update and display daily scores"""
        # Clear previous
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Calculate current player score
        current_score = 0
        if self.today in self.logs:
            current_score = self.logs[self.today].get("total_points", 0)
        else:
            current_score = sum(t.points for t in self.tasks if t.id in self.completed_selected)
        
        # Calculate rival score
        rival_score = 0
        if self.today in self.rival_logs:
            rival_score = self.rival_logs[self.today].get("total_points", 0)
        
        # Display scores
        scores_container = tk.Frame(parent, bg=self.BG_SECONDARY)
        scores_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Current player score
        tk.Label(scores_container, text=self.current_player.name.upper(), 
                bg=self.BG_SECONDARY, fg=self.FG_COLOR, font=("Menlo", 10, "bold")).pack(side=tk.LEFT)
        tk.Label(scores_container, text=f"{current_score} pts", 
                bg=self.BG_SECONDARY, fg=self.POSITIVE_COLOR, font=("Menlo", 14, "bold")).pack(side=tk.LEFT, padx=20)
        
        # VS
        tk.Label(scores_container, text="VS", 
                bg=self.BG_SECONDARY, fg=self.FG_ACCENT, font=("Menlo", 10, "bold")).pack(side=tk.LEFT, padx=10)
        
        # Rival score
        tk.Label(scores_container, text=f"{rival_score} pts", 
                bg=self.BG_SECONDARY, fg=self.POSITIVE_COLOR, font=("Menlo", 14, "bold")).pack(side=tk.LEFT, padx=20)
        tk.Label(scores_container, text=self.rival_player.name.upper(), 
                bg=self.BG_SECONDARY, fg=self.FG_COLOR, font=("Menlo", 10, "bold")).pack(side=tk.LEFT)
        
        # Winner indicator
        if current_score > rival_score:
            tk.Label(scores_container, text="🏆 WINNING!", 
                    bg=self.BG_SECONDARY, fg=self.POSITIVE_COLOR, font=("Menlo", 10, "bold")).pack(side=tk.RIGHT)
        elif rival_score > current_score:
            tk.Label(scores_container, text="🎯 Catch up!", 
                    bg=self.BG_SECONDARY, fg=self.NEGATIVE_COLOR, font=("Menlo", 10, "bold")).pack(side=tk.RIGHT)
    
    def setup_leaderboard_tab(self, parent):
        """Setup leaderboard showing statistics"""
        # Time period selection
        period_frame = tk.Frame(parent, bg=self.BG_SECONDARY)
        period_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(period_frame, text="Period:", bg=self.BG_SECONDARY, fg=self.FG_COLOR,
                font=("Menlo", 11, "bold")).pack(side=tk.LEFT, padx=5)
        
        period_var = tk.StringVar(value="today")
        for period in ["today", "this_week", "this_month", "all_time"]:
            tk.Radiobutton(period_frame, text=period.replace("_", " ").title(), 
                          variable=period_var, value=period,
                          bg=self.BG_SECONDARY, fg=self.FG_COLOR, selectcolor=self.BG_COLOR,
                          font=("Menlo", 10),
                          command=lambda: self.refresh_leaderboard(parent, period_var.get())).pack(side=tk.LEFT, padx=10)
        
        # Leaderboard content
        content_frame = tk.Frame(parent, bg=self.BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.leaderboard_frame = content_frame
        self.refresh_leaderboard(content_frame, "today")
    
    def refresh_leaderboard(self, parent, period):
        """Refresh leaderboard based on period"""
        # Clear
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Calculate scores based on period
        if period == "today":
            current_score = self.logs.get(self.today, {}).get("total_points", 0)
            rival_score = self.rival_logs.get(self.today, {}).get("total_points", 0)
        elif period == "this_week":
            current_score = self.weekly_logs.get(self.current_week, {}).get("total_points", 0)
            rival_score = self.rival_weekly_logs.get(self.current_week, {}).get("total_points", 0)
        elif period == "this_month":
            current_score = self.monthly_logs.get(self.current_month, {}).get("total_points", 0)
            rival_score = self.rival_monthly_logs.get(self.current_month, {}).get("total_points", 0)
        else:  # all_time
            current_score = sum(log.get("total_points", 0) for log in self.logs.values())
            rival_score = sum(log.get("total_points", 0) for log in self.rival_logs.values())
        
        # Create leaderboard
        scores = [
            (self.current_player.name, current_score, self.current_player.id),
            (self.rival_player.name, rival_score, self.rival_player.id)
        ]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Display
        for rank, (name, score, player_id) in enumerate(scores, 1):
            frame = tk.Frame(parent, bg=self.BG_SECONDARY, relief="raised", bd=1)
            frame.pack(fill=tk.X, pady=10, padx=10)
            
            inner = tk.Frame(frame, bg=self.BG_SECONDARY, padx=20, pady=15)
            inner.pack(fill=tk.BOTH, expand=True)
            
            # Rank
            tk.Label(inner, text=f"#{rank}", bg=self.BG_SECONDARY, fg=self.FG_ACCENT,
                    font=("Menlo", 14, "bold")).pack(side=tk.LEFT, padx=10)
            
            # Name
            tk.Label(inner, text=name, bg=self.BG_SECONDARY, fg=self.FG_COLOR,
                    font=("Menlo", 12, "bold")).pack(side=tk.LEFT, padx=20)
            
            # Score
            score_color = self.POSITIVE_COLOR if score >= 0 else self.NEGATIVE_COLOR
            tk.Label(inner, text=f"{score} pts", bg=self.BG_SECONDARY, fg=score_color,
                    font=("Menlo", 14, "bold")).pack(side=tk.RIGHT, padx=10)
            
            # Trophy for first place
            if rank == 1:
                tk.Label(inner, text="🏆", bg=self.BG_SECONDARY, font=("Menlo", 16)).pack(side=tk.RIGHT, padx=5)
    
    def setup_weekly_tab(self, parent):
        """Setup weekly goals tab"""
        tk.Label(parent, text="Weekly Goals Coming Soon", 
                bg=self.BG_COLOR, fg=self.FG_COLOR, font=("Menlo", 12)).pack(pady=50)
    
    def setup_monthly_tab(self, parent):
        """Setup monthly goals tab"""
        tk.Label(parent, text="Monthly Goals Coming Soon", 
                bg=self.BG_COLOR, fg=self.FG_COLOR, font=("Menlo", 12)).pack(pady=50)
    
    def refresh_ui(self):
        """Refresh the entire UI"""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_ui()


def main():
    root = tk.Tk()
    app = MultiplayerTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
