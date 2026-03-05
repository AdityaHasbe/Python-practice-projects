import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Tic-Tac-Toe")
        self.root.geometry("550x650")
        self.root.configure(bg="#1E1E2E") # Dark modern background

        # Game State Variables
        self.mode = None
        self.p1_name = ""
        self.p2_name = ""
        self.rps_p1_choice = None
        self.first_player = ""
        self.second_player = ""
        self.first_player_symbol = ""
        self.second_player_symbol = ""

        self.current_turn_name = ""
        self.current_turn_symbol = ""
        self.board = [""] * 9
        self.buttons = []

        # Main frame to hold our changing screens
        self.main_frame = tk.Frame(self.root, bg="#1E1E2E")
        self.main_frame.pack(expand=True, fill="both")

        self.show_welcome_screen()

    def clear_frame(self):
        """Destroys all widgets in the main frame to prepare for the next screen."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # --- SCREEN 1: Welcome & Mode Selection ---
    def show_welcome_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Welcome to the Tic Tac Toe Game", font=("Helvetica", 22, "bold"), bg="#1E1E2E", fg="#00E5FF").pack(pady=50)

        tk.Button(self.main_frame, text="Play with Computer", font=("Helvetica", 16, "bold"), bg="#FF007F", fg="white", width=20, command=lambda: self.setup_mode("Computer")).pack(pady=15)
        tk.Button(self.main_frame, text="Two Player Game", font=("Helvetica", 16, "bold"), bg="#39FF14", fg="black", width=20, command=lambda: self.setup_mode("Player")).pack(pady=15)

    def setup_mode(self, mode):
        self.mode = mode
        self.show_name_screen()

    # --- SCREEN 2: Name Entry ---
    def show_name_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Enter Player Names", font=("Helvetica", 22, "bold"), bg="#1E1E2E", fg="#00E5FF").pack(pady=40)

        tk.Label(self.main_frame, text="Player 1 Name:", font=("Helvetica", 14), bg="#1E1E2E", fg="white").pack()
        self.e1 = tk.Entry(self.main_frame, font=("Helvetica", 16), justify="center")
        self.e1.pack(pady=10)

        if self.mode == "Player":
            tk.Label(self.main_frame, text="Player 2 Name:", font=("Helvetica", 14), bg="#1E1E2E", fg="white").pack()
            self.e2 = tk.Entry(self.main_frame, font=("Helvetica", 16), justify="center")
            self.e2.pack(pady=10)
        else:
            self.p2_name = "Computer"

        tk.Button(self.main_frame, text="Continue", font=("Helvetica", 14, "bold"), bg="#FADA5E", fg="black", width=15, command=self.save_names).pack(pady=30)

    def save_names(self):
        self.p1_name = self.e1.get().strip() or "Player 1"
        if self.mode == "Player":
            self.p2_name = self.e2.get().strip() or "Player 2"
        self.show_rps_screen()

    # --- SCREEN 3: Rock Paper Scissors ---
    def show_rps_screen(self, msg="Time for Rock-Paper-Scissors\nto decide who goes first!"):
        self.clear_frame()
        tk.Label(self.main_frame, text=msg, font=("Helvetica", 18, "bold"), bg="#1E1E2E", fg="#FFD700", wraplength=450, justify="center").pack(pady=30)

        current_chooser = self.p1_name if self.rps_p1_choice is None else self.p2_name
        tk.Label(self.main_frame, text=f"{current_chooser}, select your move:", font=("Helvetica", 16), bg="#1E1E2E", fg="white").pack(pady=15)

        btn_frame = tk.Frame(self.main_frame, bg="#1E1E2E")
        btn_frame.pack(pady=20)

        choices = ["Rock", "Paper", "Scissors"]
        colors = ["#FF4500", "#1E90FF", "#32CD32"]
        
        for i, choice in enumerate(choices):
            tk.Button(btn_frame, text=choice, font=("Helvetica", 14, "bold"), bg=colors[i], fg="white", width=10, command=lambda c=choice: self.handle_rps(c)).grid(row=0, column=i, padx=10)

    def handle_rps(self, choice):
        if self.rps_p1_choice is None:
            self.rps_p1_choice = choice
            if self.mode == "Computer":
                comp_choice = random.choice(["Rock", "Paper", "Scissors"])
                self.evaluate_rps(self.rps_p1_choice, comp_choice)
            else:
                self.show_rps_screen(msg="Player 1 has chosen.\nNow it's Player 2's turn!")
        else:
            self.evaluate_rps(self.rps_p1_choice, choice)

    def evaluate_rps(self, c1, c2):
        self.rps_p1_choice = None # Reset in case of a tie
        
        if c1 == c2:
            messagebox.showinfo("Draw", f"Both chose {c1}! It's a tie, try again.")
            self.show_rps_screen("It was a tie! Go again.")
            return

        p1_wins = (c1 == "Rock" and c2 == "Scissors") or \
                  (c1 == "Paper" and c2 == "Rock") or \
                  (c1 == "Scissors" and c2 == "Paper")

        if p1_wins:
            winner, loser = self.p1_name, self.p2_name
        else:
            winner, loser = self.p2_name, self.p1_name

        self.first_player = winner
        self.second_player = loser

        messagebox.showinfo("Result", f"{self.p1_name} chose {c1}\n{self.p2_name} chose {c2}\n\n{winner} wins the toss!")

        if winner == "Computer":
            self.first_player_symbol = "X"
            self.second_player_symbol = "O"
            self.start_tictactoe()
        else:
            self.show_symbol_choice(winner)

    # --- SCREEN 4: Symbol Choice ---
    def show_symbol_choice(self, winner_name):
        self.clear_frame()
        tk.Label(self.main_frame, text=f"{winner_name}, choose your symbol:", font=("Helvetica", 20, "bold"), bg="#1E1E2E", fg="#00E5FF").pack(pady=50)

        tk.Button(self.main_frame, text="X", font=("Helvetica", 30, "bold"), bg="#FF007F", fg="white", width=5, command=lambda: self.set_symbols("X")).pack(pady=15)
        tk.Button(self.main_frame, text="O", font=("Helvetica", 30, "bold"), bg="#39FF14", fg="black", width=5, command=lambda: self.set_symbols("O")).pack(pady=15)

    def set_symbols(self, choice):
        self.first_player_symbol = choice
        self.second_player_symbol = "O" if choice == "X" else "X"
        self.start_tictactoe()

    # --- SCREEN 5: The Game Grid ---
    def start_tictactoe(self):
        self.current_turn_name = self.first_player
        self.current_turn_symbol = self.first_player_symbol
        self.board = [""] * 9
        self.show_tictactoe_screen()

    def show_tictactoe_screen(self):
        self.clear_frame()
        self.turn_label = tk.Label(self.main_frame, text=f"{self.current_turn_name}'s Turn ({self.current_turn_symbol})", font=("Helvetica", 20, "bold"), bg="#1E1E2E", fg="#FFD700")
        self.turn_label.pack(pady=20)

        grid_frame = tk.Frame(self.main_frame, bg="black") # Black borders for the grid
        grid_frame.pack()

        self.buttons = []
        for i in range(9):
            btn = tk.Button(grid_frame, text="", font=("Helvetica", 36, "bold"), width=4, height=2, bg="#FFFFFF", activebackground="#D3D3D3", command=lambda idx=i: self.on_grid_click(idx))
            btn.grid(row=i//3, column=i%3, padx=3, pady=3)
            self.buttons.append(btn)

        if self.current_turn_name == "Computer":
            self.root.after(600, self.computer_move) # 600ms delay so it doesn't happen instantly

    def on_grid_click(self, idx):
        if self.board[idx] == "" and self.current_turn_name != "Computer":
            self.make_move(idx)

    def make_move(self, idx):
        self.board[idx] = self.current_turn_symbol
        color = "#FF007F" if self.current_turn_symbol == "X" else "#39FF14"
        self.buttons[idx].config(text=self.current_turn_symbol, fg=color, state="disabled")

        if self.check_win():
            winner = self.current_turn_name
            loser = self.second_player if winner == self.first_player else self.first_player
            messagebox.showinfo("Game Over", f"Congratulations! {winner} won and {loser} lost.")
            self.show_welcome_screen() # Restart Game
        elif "" not in self.board:
            messagebox.showinfo("Game Over", "It's a draw! Well played.")
            self.show_welcome_screen() # Restart Game
        else:
            self.switch_turn()

    def switch_turn(self):
        if self.current_turn_name == self.first_player:
            self.current_turn_name = self.second_player
            self.current_turn_symbol = self.second_player_symbol
        else:
            self.current_turn_name = self.first_player
            self.current_turn_symbol = self.first_player_symbol

        self.turn_label.config(text=f"{self.current_turn_name}'s Turn ({self.current_turn_symbol})")

        if self.current_turn_name == "Computer":
            self.root.after(600, self.computer_move)

    def computer_move(self):
        # The computer picks a random available square
        available_spots = [i for i, val in enumerate(self.board) if val == ""]
        if available_spots:
            idx = random.choice(available_spots)
            self.make_move(idx)

    def check_win(self):
        winning_combinations = [
            (0,1,2), (3,4,5), (6,7,8), # Rows
            (0,3,6), (1,4,7), (2,5,8), # Columns
            (0,4,8), (2,4,6)           # Diagonals
        ]
        for a, b, c in winning_combinations:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()