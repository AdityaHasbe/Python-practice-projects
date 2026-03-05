import tkinter as tk
from tkinter import messagebox
import random

# Attempt to load built-in sound for Windows
try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

# ==========================================
# GLOBAL STATE & STYLES
# ==========================================
solution_board = []    
puzzle_board = []      
cells = [[None for _ in range(9)] for _ in range(9)]
string_vars = [[None for _ in range(9)] for _ in range(9)]

mistakes = 0
hints_left = 3
elapsed_time = 0
timer_id = None
is_playing_game = False

# --- UI Palette & Fonts ---
BG_COLOR = "#F0F4F8"       
TEXT_COLOR = "#2C3E50"     
USER_INPUT = "#2980B9"     
ERROR_COLOR = "#E74C3C"    
GRID_LINE = "#34495E"      
CELL_LINE = "#BDC3C7"      

FONT_TITLE = ("Segoe UI", 28, "bold")  # Slightly smaller to save space
FONT_HEADING = ("Segoe UI", 14)
FONT_BTN = ("Segoe UI", 12, "bold")
FONT_GRID = ("Segoe UI", 20, "bold")   # Reduced to fit smaller screens

# ==========================================
# 1. CORE LOGIC
# ==========================================

def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None

def is_valid(board, row, col, num):
    if num in board[row]: return False
    for i in range(9):
        if board[i][col] == num: return False
    box_x, box_y = (col // 3) * 3, (row // 3) * 3
    for i in range(box_y, box_y + 3):
        for j in range(box_x, box_x + 3):
            if board[i][j] == num: return False
    return True

def fill_board(board):
    empty = find_empty(board)
    if not empty: return True
    r, c = empty
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(numbers)
    for i in numbers:
        if is_valid(board, r, c, i):
            board[r][c] = i
            if fill_board(board): return True
            board[r][c] = 0
    return False

def solve_board(board):
    """A deterministic solver used to find the solution for pre-made extreme boards."""
    empty = find_empty(board)
    if not empty: return True
    r, c = empty
    for i in range(1, 10):
        if is_valid(board, r, c, i):
            board[r][c] = i
            if solve_board(board): return True
            board[r][c] = 0
    return False

def count_solutions(board):
    empty = find_empty(board)
    if not empty: return 1
    r, c = empty
    count = 0
    for i in range(1, 10):
        if is_valid(board, r, c, i):
            board[r][c] = i
            count += count_solutions(board)
            board[r][c] = 0
            if count > 1: return count
    return count

def generate_super_extreme():
    """Uses a seed transformation technique to instantly generate 17-20 clue boards."""
    global solution_board, puzzle_board
    
    # A mathematically proven 17-clue base puzzle
    board = [
        [0,0,0, 8,0,1, 0,0,0],
        [0,0,0, 0,0,0, 0,4,3],
        [5,0,0, 0,0,0, 0,0,0],
        [0,0,0, 0,7,0, 8,0,0],
        [0,0,0, 0,0,0, 1,0,0],
        [0,2,0, 0,3,0, 0,0,0],
        [6,0,0, 0,0,0, 0,7,5],
        [0,0,3, 4,0,0, 0,0,0],
        [0,0,0, 2,0,0, 6,0,0]
    ]
    
    # 1. Permute numbers (Swap symbols so the pattern changes)
    nums = list(range(1, 10))
    random.shuffle(nums)
    mapping = {i+1: nums[i] for i in range(9)}
    mapping[0] = 0
    
    for r in range(9):
        for c in range(9):
            board[r][c] = mapping[board[r][c]]
            
    # 2. Rotate board randomly (0 to 3 times)
    for _ in range(random.randint(0, 3)):
        board = [list(x) for x in zip(*board[::-1])]
        
    # 3. Solve a copy to establish the true solution
    sol_board = [r[:] for r in board]
    solve_board(sol_board)
    
    # 4. Add 0 to 3 extra clues randomly to make it 17-20 clues total
    extra_clues = random.randint(0, 3)
    empty_cells = [(r, c) for r in range(9) for c in range(9) if board[r][c] == 0]
    random.shuffle(empty_cells)
    
    for i in range(extra_clues):
        r, c = empty_cells[i]
        board[r][c] = sol_board[r][c]
        
    solution_board = sol_board
    puzzle_board = [r[:] for r in board]
    return board

def generate_puzzle(difficulty):
    global solution_board, puzzle_board
    
    if difficulty == "super_extreme":
        return generate_super_extreme()
    
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_board(board)
    solution_board = [r[:] for r in board] 
    
    if difficulty == "easy": target_removed = 30
    elif difficulty == "medium": target_removed = 40
    elif difficulty == "hard": target_removed = 48
    elif difficulty == "extreme": target_removed = 54
    else: target_removed = 35
        
    cells_list = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells_list)
    removed = 0
    
    for row, col in cells_list:
        if removed >= target_removed: break
        backup = board[row][col]
        board[row][col] = 0
        test_board = [r[:] for r in board]
        if count_solutions(test_board) != 1:
            board[row][col] = backup
        else:
            removed += 1
            
    puzzle_board = [r[:] for r in board]
    return board

# ==========================================
# 2. AUDIO & TIMER FUNCTIONS
# ==========================================

def play_buzzer():
    if HAS_SOUND: winsound.Beep(300, 300) 

def play_win_sound():
    if HAS_SOUND:
        winsound.Beep(523, 150)
        winsound.Beep(659, 150)
        winsound.Beep(784, 150)
        winsound.Beep(1046, 300) 

def update_timer():
    global elapsed_time, timer_id
    if is_playing_game:
        elapsed_time += 1
        mins, secs = divmod(elapsed_time, 60)
        lbl_timer.config(text=f"⏱️ Time: {mins:02d}:{secs:02d}")
        timer_id = root.after(1000, update_timer)

def stop_timer():
    global timer_id
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None

# ==========================================
# 3. GAMEPLAY MECHANICS
# ==========================================

def check_input(event, r, c):
    global mistakes
    val = string_vars[r][c].get().strip()
    
    if val == "": 
        cells[r][c].config(fg=USER_INPUT) 
        return
        
    if not val.isdigit() or len(val) > 1 or val == "0":
        string_vars[r][c].set("")
        return
        
    if not is_playing_game: 
        return 
        
    entered_num = int(val)
    
    if entered_num != solution_board[r][c]:
        string_vars[r][c].set("") 
        cells[r][c].config(fg=ERROR_COLOR)
        
        cells[r][c].insert(0, str(entered_num))
        root.update()
        play_buzzer()
        root.after(400, lambda: string_vars[r][c].set(""))
        
        mistakes += 1
        lbl_mistakes.config(text=f"❌ Mistakes: {mistakes}/3")
        
        if mistakes >= 3:
            game_over()
    else:
        cells[r][c].config(fg=USER_INPUT, state="disabled", disabledforeground=USER_INPUT)
        check_win_and_autocomplete()

def use_hint():
    global hints_left
    if hints_left <= 0 or not is_playing_game: return
    
    empty_cells = [(r, c) for r in range(9) for c in range(9) if string_vars[r][c].get() == ""]
    if not empty_cells: return
    
    r, c = random.choice(empty_cells)
    correct_num = solution_board[r][c]
    
    cells[r][c].config(state="normal")
    string_vars[r][c].set(str(correct_num))
    cells[r][c].config(fg=USER_INPUT, state="disabled", disabledforeground=USER_INPUT)
    
    hints_left -= 1
    btn_hint.config(text=f"💡 Hint ({hints_left})")
    
    check_win_and_autocomplete()

def check_win_and_autocomplete():
    empty_count = sum(1 for r in range(9) for c in range(9) if string_vars[r][c].get() == "")
    if empty_count == 0: win_game()
    elif empty_count <= 4: autocomplete()

def autocomplete():
    for r in range(9):
        for c in range(9):
            if string_vars[r][c].get() == "":
                cells[r][c].config(state="normal")
                string_vars[r][c].set(str(solution_board[r][c]))
                cells[r][c].config(fg=USER_INPUT, state="disabled", disabledforeground=USER_INPUT)
                root.update()
                root.after(100) 
    win_game()

def win_game():
    stop_timer()
    play_win_sound()
    mins, secs = divmod(elapsed_time, 60)
    messagebox.showinfo("Victory!", f"Congratulations! You solved it in {mins:02d}:{secs:02d}.")
    show_menu()

def game_over():
    stop_timer()
    play_buzzer()
    response = messagebox.askyesno("Game Over", "You made 3 mistakes. Game Over!\n\nWould you like to see the solution?")
    if response:
        for r in range(9):
            for c in range(9):
                cells[r][c].config(state="normal")
                string_vars[r][c].set(str(solution_board[r][c]))
                cells[r][c].config(fg="#7F8C8D", state="disabled")
    else:
        show_menu()

# ==========================================
# 4. GUI NAVIGATION & SETUP
# ==========================================

def hide_all_frames():
    frame_menu.pack_forget()
    frame_diff.pack_forget()
    frame_stats.pack_forget()
    grid_frame.pack_forget()
    frame_game_controls.pack_forget()
    frame_solve_controls.pack_forget()
    lbl_loading.pack_forget()

def show_menu():
    stop_timer()
    hide_all_frames()
    frame_menu.pack(pady=10)

def show_difficulties():
    hide_all_frames()
    frame_diff.pack(pady=10)

def start_game(difficulty):
    global mistakes, hints_left, elapsed_time, is_playing_game
    mistakes = 0
    hints_left = 3
    elapsed_time = 0
    is_playing_game = True
    
    lbl_mistakes.config(text="❌ Mistakes: 0/3")
    btn_hint.config(text="💡 Hint (3)")
    lbl_timer.config(text="⏱️ Time: 00:00")
    
    hide_all_frames()
    
    lbl_loading.pack(pady=50)
    root.update()
    
    board = generate_puzzle(difficulty)
    populate_gui_board(board, disable_filled=True)
    
    lbl_loading.pack_forget() 
    frame_stats.pack(pady=5)
    grid_frame.pack(pady=5)
    frame_game_controls.pack(pady=10)
    
    update_timer()

def start_solve_mode():
    global is_playing_game
    is_playing_game = False
    
    hide_all_frames()
    
    empty_board = [[0 for _ in range(9)] for _ in range(9)]
    populate_gui_board(empty_board, disable_filled=False)
    
    grid_frame.pack(pady=10)
    frame_solve_controls.pack(pady=10)
    
    messagebox.showinfo("Solve Mode", "Enter the numbers of your puzzle into the grid, then click 'Solve it!'.")

def populate_gui_board(board, disable_filled):
    for r in range(9):
        for c in range(9):
            cells[r][c].config(state="normal", fg=USER_INPUT)
            if board[r][c] != 0:
                string_vars[r][c].set(str(board[r][c]))
                if disable_filled:
                    cells[r][c].config(state="disabled", disabledforeground=TEXT_COLOR)
            else:
                string_vars[r][c].set("")

def execute_solver():
    board = [[0 for _ in range(9)] for _ in range(9)]
    for r in range(9):
        for c in range(9):
            val = string_vars[r][c].get()
            if val.isdigit(): board[r][c] = int(val)
            else: board[r][c] = 0
            
    for r in range(9):
        for c in range(9):
            num = board[r][c]
            if num != 0:
                board[r][c] = 0
                if not is_valid(board, r, c, num):
                    messagebox.showerror("Error", "Invalid starting board! Check your numbers.")
                    return
                board[r][c] = num
                
    if solve_board(board):
        populate_gui_board(board, disable_filled=True)
        messagebox.showinfo("Solved", "Here is your solution!")
    else:
        messagebox.showerror("Error", "This puzzle has no mathematically valid solution.")

def create_button(parent, text, color, command, width=20):
    return tk.Button(parent, text=text, font=FONT_BTN, bg=color, fg="white", 
                     command=command, width=width, relief="flat", cursor="hand2", pady=3)

# ==========================================
# 5. DRAWING THE WINDOW (Component Construction)
# ==========================================

root = tk.Tk()
root.title("Python Pro Sudoku")
# Reduced window height so it doesn't clip off the screen
root.geometry("520x680") 
root.configure(bg=BG_COLOR)

# 1. Title
tk.Label(root, text="SUDOKU", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(10, 5))

# 2. Loading Label
lbl_loading = tk.Label(root, text="Calculating puzzle geometry...\nPlease wait.", font=FONT_HEADING, bg=BG_COLOR, fg="#D35400")

# 3. Menu Frame
frame_menu = tk.Frame(root, bg=BG_COLOR)
tk.Label(frame_menu, text="Choose a game mode:", bg=BG_COLOR, font=FONT_HEADING, fg=TEXT_COLOR).pack(pady=(0,10))
create_button(frame_menu, "Play a Puzzle", "#2980B9", show_difficulties).pack(pady=5)
create_button(frame_menu, "Solve for Me", "#7F8C8D", start_solve_mode).pack(pady=5)

# 4. Difficulty Frame
frame_diff = tk.Frame(root, bg=BG_COLOR)
tk.Label(frame_diff, text="Select Difficulty:", bg=BG_COLOR, font=FONT_HEADING, fg=TEXT_COLOR).pack(pady=(0,5))
create_button(frame_diff, "Easy", "#27AE60", lambda: start_game("easy")).pack(pady=2)
create_button(frame_diff, "Medium", "#F39C12", lambda: start_game("medium")).pack(pady=2)
create_button(frame_diff, "Hard", "#E67E22", lambda: start_game("hard")).pack(pady=2)
create_button(frame_diff, "Extreme", "#C0392B", lambda: start_game("extreme")).pack(pady=2)
create_button(frame_diff, "Super Extreme", "#8E44AD", lambda: start_game("super_extreme")).pack(pady=2)
tk.Button(frame_diff, text="← Back", font=("Segoe UI", 10, "underline"), bg=BG_COLOR, fg=TEXT_COLOR, relief="flat", cursor="hand2", command=show_menu).pack(pady=5)

# 5. Stats Frame
frame_stats = tk.Frame(root, bg=BG_COLOR)
lbl_mistakes = tk.Label(frame_stats, text="❌ Mistakes: 0/3", font=FONT_HEADING, fg=ERROR_COLOR, bg=BG_COLOR)
lbl_mistakes.grid(row=0, column=0, padx=20)
lbl_timer = tk.Label(frame_stats, text="⏱️ Time: 00:00", font=FONT_HEADING, fg=TEXT_COLOR, bg=BG_COLOR)
lbl_timer.grid(row=0, column=1, padx=20)

# 6. Grid Frame
grid_frame = tk.Frame(root, bg=GRID_LINE, bd=3) 
for r_block in range(3):
    for c_block in range(3):
        block_frame = tk.Frame(grid_frame, bg=GRID_LINE)
        block_frame.grid(row=r_block, column=c_block, padx=1, pady=1)
        
        for r_cell in range(3):
            for c_cell in range(3):
                r = r_block * 3 + r_cell
                c = c_block * 3 + c_cell
                
                cell_frame = tk.Frame(block_frame, bg=CELL_LINE) 
                cell_frame.grid(row=r_cell, column=c_cell, padx=1, pady=1)
                
                sv = tk.StringVar()
                string_vars[r][c] = sv
                
                # Removed inner padding to shrink grid height
                entry = tk.Entry(cell_frame, textvariable=sv, width=2, font=FONT_GRID, 
                                 justify='center', bg="white", fg=USER_INPUT, 
                                 disabledbackground="#FDFDFD", relief="flat", highlightthickness=0)
                entry.pack(padx=1, pady=1) 
                entry.bind('<KeyRelease>', lambda event, row=r, col=c: check_input(event, row, col))
                cells[r][c] = entry

# 7. Bottom Controls (Game Mode)
frame_game_controls = tk.Frame(root, bg=BG_COLOR)
btn_hint = create_button(frame_game_controls, "💡 Hint (3)", "#F1C40F", use_hint, width=12)
btn_hint.config(fg=TEXT_COLOR) 
btn_hint.grid(row=0, column=0, padx=10)
create_button(frame_game_controls, "Quit", "#E74C3C", show_menu, width=12).grid(row=0, column=1, padx=10)

# 8. Bottom Controls (Solve Mode)
frame_solve_controls = tk.Frame(root, bg=BG_COLOR)
create_button(frame_solve_controls, "Solve it!", "#27AE60", execute_solver, width=15).grid(row=0, column=0, padx=10)
create_button(frame_solve_controls, "Cancel", "#E74C3C", show_menu, width=15).grid(row=0, column=1, padx=10)

# Initialize the UI by showing only the menu
show_menu()

root.mainloop()