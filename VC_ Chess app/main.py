import sys
import threading
import random
import chess
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox, QPushButton, QFileDialog, QStackedWidget, QSlider, QLabel, QFrame, QComboBox, QDialog, QListWidget
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject

from engine.game_state import GameState
from engine.stockfish_handler import StockfishHandler
from ui.board_widget import BoardWidget
from ui.sidebars import EvaluationBar 

class AIWorker(QObject):
    """Worker thread for AI calculations."""
    move_ready = pyqtSignal(str)
    
    def __init__(self, stockfish, fen):
        super().__init__()
        self.stockfish = stockfish
        self.fen = fen
    
    def run(self):
        """Run AI move calculation."""
        self.stockfish.set_fen_position(self.fen)
        best_move = self.stockfish.get_best_move()
        if best_move:
            self.move_ready.emit(best_move)


class EvaluationWorker(QObject):
    """Compute a Stockfish evaluation in a thread."""
    eval_ready = pyqtSignal(dict, bool)          # eval_data, is_white_turn

    def __init__(self, stockfish, fen, is_white):
        super().__init__()
        self.stockfish = stockfish
        self.fen = fen
        self.is_white = is_white

    def run(self):
        self.stockfish.set_fen_position(self.fen)
        eval_data = self.stockfish.get_evaluation()
        self.eval_ready.emit(eval_data, self.is_white)


class PGNLoader(QObject):
    """Parse a PGN string off the main thread."""
    finished = pyqtSignal(list)
    error = pyqtSignal(Exception)

    def __init__(self, game_state, pgn_string):
        super().__init__()
        self.game_state = game_state
        self.pgn = pgn_string

    def run(self):
        try:
            positions = self.game_state.load_pgn(self.pgn)
            self.finished.emit(positions)
        except Exception as e:
            self.error.emit(e)


class OpeningFetcher(QObject):
    """Fetch an opening from the Lichess explorer API."""
    fetched = pyqtSignal(str)          # PGN text
    error   = pyqtSignal(Exception)

    def __init__(self, eco_code):
        super().__init__()
        self.eco = eco_code

    def run(self):
        import requests, chess, chess.pgn
        try:
            url = f"https://explorer.lichess.ovh/masters?eco={self.eco}"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            moves = data.get("moves", [])[:8]   # first eight half‑moves
            board = chess.Board()
            game = chess.pgn.Game()
            node = game
            for m in moves:
                mv = chess.Move.from_uci(m["uci"])
                node = node.add_variation(mv)
                board.push(mv)
            self.fetched.emit(str(game))
        except Exception as e:
            self.error.emit(e)

class ChessAppMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Python Chess & Game Review")
        self.setGeometry(100, 100, 900, 700) 
        self.setStyleSheet("background-color: #2b2b2b;") 

        self.game_state = GameState()
        self.stockfish = StockfishHandler(elo=1500) 
        
        # Game state
        self.game_mode = None
        self.game_active = False
        self.game_over_flag = False
        self.game_result = None
        self.ai_thinking = False
        
        # Time control
        self.time_control = 300  # seconds (5 minutes default)
        self.white_time = self.time_control
        self.black_time = self.time_control
        self.game_timer = None
        self.elo_strength = 1500  # default ELO
        
        # Opening Trainer mode
        self.training_score = 0
        self.training_mistakes = 0
        
        # Puzzle mode
        self.puzzle_difficulty = 0
        self.puzzle_score = 0
        self.puzzle_solution_shown = False
        self.puzzle_fen = None
        self.puzzle_solution = []
        self.puzzle_solution_san = []
        self.puzzle_name = ""

        # Create widgets
        self.board_widget = BoardWidget(self.game_state)
        self.eval_bar = EvaluationBar()
        self.board_widget.move_requested.connect(self.handle_user_move)

        # Use QStackedWidget for clean screen switching
        self.stacked_widget = QStackedWidget()
        
        # Screen 0: Main Menu
        self.menu_screen = self.create_menu_screen()
        self.stacked_widget.addWidget(self.menu_screen)
        
        # Screen 1: Settings Screen (will be created dynamically in show_settings())
        # Placeholder widget that will be replaced
        self.settings_screen = QWidget()
        self.stacked_widget.addWidget(self.settings_screen)
        
        # Screen 2: Game Board
        self.game_screen = self.create_game_screen()
        self.stacked_widget.addWidget(self.game_screen)
        
        self.setCentralWidget(self.stacked_widget)
        self.show_menu()

    def create_menu_screen(self):
        """Create the main menu screen."""
        menu_widget = QWidget()
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(20, 20, 20, 20)
        menu_layout.addStretch()
        
        # Title
        title = QLabel("♟ CHESS CHAMPION ♟")
        title.setStyleSheet("color: #FF007F; font-size: 36px; font-weight: bold; text-align: center;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_layout.addWidget(title)
        
        menu_layout.addSpacing(40)
        
        button_style = """
            QPushButton {
                background-color: #FF007F;
                color: white;
                padding: 15px;
                font-weight: bold;
                font-size: 16px;
                border-radius: 8px;
                min-width: 350px;
                min-height: 50px;
                border: 2px solid transparent;
            }
            QPushButton:hover {
                background-color: #FF0099;
                border: 2px solid #FFFFFF;
            }
            QPushButton:pressed {
                background-color: #DD0080;
            }
        """
        
        btn_computer = QPushButton("⚔ Play vs Stockfish")
        btn_computer.setStyleSheet(button_style)
        btn_computer.clicked.connect(self.start_vs_computer)
        
        btn_local = QPushButton("👥 Play vs Local Friend")
        style_local = button_style.replace("#FF007F", "#39FF14").replace("#FF0099", "#44FF22").replace("#DD0080", "#22DD00")
        style_local = style_local.replace("white;", "black;")
        btn_local.setStyleSheet(style_local)
        btn_local.clicked.connect(self.start_vs_local)
        
        btn_opening = QPushButton("🎯 Opening Trainer")
        style_opening = button_style.replace("#FF007F", "#FF8C00").replace("#FF0099", "#FFA500").replace("#DD0080", "#DD6600")
        btn_opening.setStyleSheet(style_opening)
        btn_opening.clicked.connect(self.start_opening_trainer)
        
        btn_puzzle = QPushButton("🧩 Puzzle Mode")
        style_puzzle = button_style.replace("#FF007F", "#9C27B0").replace("#FF0099", "#BA68C8").replace("#DD0080", "#8B008B")
        btn_puzzle.setStyleSheet(style_puzzle)
        btn_puzzle.clicked.connect(self.start_puzzle_mode)
        
        btn_review = QPushButton("📚 Game Review (PGN)")
        style_review = button_style.replace("#FF007F", "#4169E1").replace("#FF0099", "#5179F9").replace("#DD0080", "#2050C0")
        btn_review.setStyleSheet(style_review)
        btn_review.clicked.connect(self.start_game_review)
        
        center_layout = QHBoxLayout()
        button_box = QVBoxLayout()
        button_box.setSpacing(20)
        button_box.addWidget(btn_computer)
        button_box.addWidget(btn_local)
        button_box.addWidget(btn_opening)
        button_box.addWidget(btn_puzzle)
        button_box.addWidget(btn_review)
        button_box.addStretch()
        
        center_layout.addStretch()
        center_layout.addLayout(button_box)
        center_layout.addStretch()
        
        menu_layout.addLayout(center_layout)
        menu_layout.addStretch()
        
        menu_widget.setLayout(menu_layout)
        return menu_widget

    def create_settings_screen(self):
        """Create the settings screen for ELO and time selection."""
        settings_widget = QWidget()
        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(30)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        settings_layout.addStretch()
        
        # Title
        title = QLabel("Game Settings")
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_layout.addWidget(title)
        
        settings_layout.addSpacing(20)
        
        # ELO Selection with Slider (for computer vs computer mode)
        if self.game_mode == "computer":
            elo_section = QVBoxLayout()
            elo_title = QLabel("Engine Difficulty")
            elo_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
            elo_section.addWidget(elo_title)
            
            # Slider for ELO
            self.elo_slider = QSlider(Qt.Orientation.Horizontal)
            # Stockfish Python wrapper enforces a minimum Elo of 1320, so
            # we prevent the user from sliding below that value.
            self.elo_slider.setMinimum(1320)
            self.elo_slider.setMaximum(3000)
            self.elo_slider.setValue(1500)
            self.elo_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            self.elo_slider.setTickInterval(200)
            self.elo_slider.setStyleSheet("""
                QSlider::groove:horizontal {
                    background-color: #555;
                    height: 8px;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background-color: #FF007F;
                    width: 18px;
                    margin: -5px 0;
                    border-radius: 9px;
                }
                QSlider::handle:horizontal:hover {
                    background-color: #FF0099;
                }
            """)
            self.elo_slider.valueChanged.connect(self.update_elo_label)
            elo_section.addWidget(self.elo_slider)
            
            # ELO value display
            elo_display_layout = QHBoxLayout()
            elo_display_layout.addStretch()
            self.elo_display_label = QLabel("1500")
            self.elo_display_label.setStyleSheet("color: #FF007F; font-size: 18px; font-weight: bold; min-width: 80px;")
            self.elo_display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            elo_display_layout.addWidget(self.elo_display_label)
            elo_display_layout.addStretch()
            elo_section.addLayout(elo_display_layout)
            
            settings_layout.addLayout(elo_section)
            settings_layout.addSpacing(20)
        
        # Time Control Selection
        time_section = QVBoxLayout()
        time_title = QLabel("Time Control")
        time_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        time_section.addWidget(time_title)
        
        time_options = [
            ("∞ No Time Limit", 0),
            ("⚡ Bullet (1 min)", 60),
            ("🏃 Blitz (3 min)", 180),
            ("✓ Rapid (5 min)", 300),
            ("📊 Standard (10 min)", 600),
            ("🕐 Classical (30 min)", 1800),
        ]
        
        for label, time_sec in time_options:
            btn = QPushButton(label)
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #444;
                    color: white;
                    padding: 10px;
                    font-weight: bold;
                    font-size: 13px;
                    border-radius: 5px;
                    border: 2px solid transparent;
                }
                QPushButton:hover {
                    background-color: #555;
                    border: 2px solid #FF007F;
                }
                QPushButton:pressed {
                    background-color: #FF007F;
                }
            """)
            btn.clicked.connect(lambda checked, t=time_sec: self.select_time_control(t))
            time_section.addWidget(btn)
        
        settings_layout.addLayout(time_section)
        settings_layout.addSpacing(20)
        
        # Back button
        btn_back = QPushButton("< Back to Menu")
        btn_back.setMinimumHeight(40)
        btn_back.setStyleSheet("""
            QPushButton {
                background-color: #cc0000;
                color: white;
                padding: 10px;
                font-weight: bold;
                font-size: 12px;
                border-radius: 5px;
                border: 2px solid transparent;
            }
            QPushButton:hover {
                background-color: #dd0000;
                border: 2px solid #ff6666;
            }
        """)
        btn_back.clicked.connect(self.show_menu)
        settings_layout.addWidget(btn_back)
        
        settings_layout.addStretch()
        
        settings_widget.setLayout(settings_layout)
        return settings_widget

    def update_elo_label(self):
        """Update ELO display when slider moves."""
        elo = self.elo_slider.value()
        self.elo_strength = elo
        self.elo_display_label.setText(str(elo))
    
    def select_time_control(self, seconds):
        """Update selected time control and start game."""
        self.time_control = seconds
        self.white_time = seconds
        self.black_time = seconds
        print(f"Selected Time Control: {seconds}s" if seconds > 0 else "No time limit")
        # Start the game after selections
        self.show_game()
        self.reset_game()

    def create_game_screen(self):
        """Create the game board screen."""
        game_widget = QWidget()
        game_layout = QVBoxLayout()
        game_layout.setSpacing(15)
        game_layout.setContentsMargins(10, 10, 10, 10)
        
        # Control panel
        control_panel = QHBoxLayout()
        control_panel.setSpacing(8)
        
        button_base_style = """
            QPushButton {
                color: white;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 11px;
                border-radius: 4px;
                min-height: 35px;
                border: 2px solid transparent;
            }
            QPushButton:hover {
                border: 2px solid #FFFFFF;
            }
            QPushButton:pressed {
                border: 2px solid #888888;
            }
        """
        
        btn_restart = QPushButton("🔄")
        btn_restart.setToolTip("New Game")
        btn_restart.setStyleSheet(button_base_style.replace("color:", "background-color: #555555; color:"))
        btn_restart.clicked.connect(self.reset_game)

        btn_resign = QPushButton("🏳")
        btn_resign.setToolTip("Resign")
        btn_resign.setStyleSheet(button_base_style.replace("color:", "background-color: #cc0000; color:"))
        btn_resign.clicked.connect(self.resign_game)

        btn_draw = QPushButton("🤝")
        btn_draw.setToolTip("Offer Draw")
        btn_draw.setStyleSheet(button_base_style.replace("color:", "background-color: #FFB90F; color: black;"))
        btn_draw.clicked.connect(self.offer_draw)

        # Puzzle helpers (enabled only when in puzzle mode)
        self.btn_hint = QPushButton("💡")
        self.btn_hint.setToolTip("Show Hint")
        self.btn_hint.setStyleSheet(button_base_style.replace("color:", "background-color: #6666cc; color: white;"))
        self.btn_hint.setEnabled(False)
        self.btn_hint.clicked.connect(self.show_puzzle_hint)

        self.btn_solution = QPushButton("📝")
        self.btn_solution.setToolTip("Show Solution")
        self.btn_solution.setStyleSheet(button_base_style.replace("color:", "background-color: #4444aa; color: white;"))
        self.btn_solution.setEnabled(False)
        self.btn_solution.clicked.connect(self.show_puzzle_solution)

        # review navigation buttons
        self.btn_prev = QPushButton("◀ Prev")
        self.btn_prev.setToolTip("Previous move")
        self.btn_prev.setStyleSheet(button_base_style.replace("color:", "background-color: #666666; color:"))
        self.btn_prev.clicked.connect(self.review_prev)
        self.btn_prev.hide()

        self.btn_next = QPushButton("Next ▶")
        self.btn_next.setToolTip("Next move")
        self.btn_next.setStyleSheet(button_base_style.replace("color:", "background-color: #666666; color:"))
        self.btn_next.clicked.connect(self.review_next)
        self.btn_next.hide()

        # Time display
        self.white_time_label = QPushButton("White: ∞")
        self.white_time_label.setToolTip("White's Time")
        self.white_time_label.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;
                color: black;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 11px;
                border-radius: 4px;
                min-height: 35px;
                border: 2px solid #666666;
            }
        """
        )
        self.white_time_label.setEnabled(False)

        self.black_time_label = QPushButton("Black: ∞")
        self.black_time_label.setToolTip("Black's Time")
        self.black_time_label.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 11px;
                border-radius: 4px;
                min-height: 35px;
                border: 2px solid #666666;
            }
        """
        )
        self.black_time_label.setEnabled(False)

        btn_menu = QPushButton("🏠")
        btn_menu.setToolTip("Main Menu")
        btn_menu.setStyleSheet(button_base_style.replace("color:", "background-color: #444444; color:"))
        btn_menu.clicked.connect(self.show_menu)

        control_panel.addWidget(btn_restart)
        control_panel.addWidget(btn_resign)
        control_panel.addWidget(btn_draw)
        control_panel.addWidget(self.btn_hint)
        control_panel.addWidget(self.btn_solution)
        control_panel.addWidget(self.btn_prev)
        control_panel.addWidget(self.btn_next)
        control_panel.addSpacing(10)
        control_panel.addWidget(self.white_time_label)
        control_panel.addWidget(self.black_time_label)
        control_panel.addStretch()
        control_panel.addWidget(btn_menu)
        
        # Board area
        board_area = QHBoxLayout()
        board_area.setSpacing(10)
        board_area.addWidget(self.eval_bar)
        board_area.addWidget(self.board_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        game_layout.addLayout(control_panel)
        game_layout.addLayout(board_area)
        
        game_widget.setLayout(game_layout)
        return game_widget

    # --- MENU NAVIGATION ---
    def show_menu(self):
        """Show the main menu."""
        self.stacked_widget.setCurrentIndex(0)
        self.cleanup_timer()
        self.game_mode = None
        self.game_active = False
        self.game_over_flag = False
        self.update_mode_buttons()

    def show_settings(self):
        """Show the settings screen (recreate to ensure correct game_mode context)."""
        # Remove old settings screen if it exists
        if self.stacked_widget.count() > 1:
            old_widget = self.stacked_widget.widget(1)
            if old_widget:
                self.stacked_widget.removeWidget(old_widget)
        
        # Create fresh settings screen with current game_mode
        self.settings_screen = self.create_settings_screen()
        self.stacked_widget.insertWidget(1, self.settings_screen)
        self.stacked_widget.setCurrentIndex(1)

    def show_game(self):
        """Show the game board."""
        self.stacked_widget.setCurrentIndex(2)

    # --- GAME MODE LOGIC ---
    def start_vs_computer(self):
        self.game_mode = "computer"
        self.show_settings()

    def start_vs_local(self):
        self.game_mode = "local"
        # For local, show settings to select time control
        self.show_settings()

    def start_opening_trainer(self):
        """prompt for an ECO code, fetch a line, load it asynchronously."""
        from PyQt6.QtWidgets import QComboBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel

        eco_codes = {
            "B01": "Scandinavian",
            "C00": "French",
            "D02": "Queen's Pawn",
            "E60": "King's Indian",
            "C50": "Italian"
        }

        dialog = QDialog(self)
        dialog.setWindowTitle("Select Opening Lesson")
        dialog.setStyleSheet("background-color: #2b2b2b; color: white;")
        layout = QVBoxLayout()
        combo = QComboBox()
        for code, name in eco_codes.items():
            combo.addItem(f"{code} – {name}", code)
        combo.setStyleSheet("""
            QComboBox { background: #444; color: white; padding: 5px; border-radius: 4px; }
            QComboBox QAbstractItemView { background: #444; color: white; }
        """)
        layout.addWidget(combo)

        btn_layout = QHBoxLayout()
        btn_start = QPushButton("Load Opening")
        btn_cancel = QPushButton("Cancel")
        btn_start.setStyleSheet("background-color: #FF007F; color: white; padding: 8px;")
        btn_cancel.setStyleSheet("background-color: #cc0000; color: white; padding: 8px;")
        btn_layout.addWidget(btn_start)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)
        dialog.setLayout(layout)

        def on_start():
            eco = combo.currentData()
            dialog.accept()
            self.statusBar().showMessage("Fetching opening from Lichess…")
            self.opening_fetcher = OpeningFetcher(eco)
            self.opening_thread = threading.Thread(target=self.opening_fetcher.run)
            self.opening_fetcher.fetched.connect(lambda p: self._async_load_pgn(p, "opening_trainer"))
            self.opening_fetcher.error.connect(lambda e: QMessageBox.warning(self, "Error", str(e)))
            self.opening_thread.daemon = True
            self.opening_thread.start()

        btn_start.clicked.connect(on_start)
        btn_cancel.clicked.connect(dialog.reject)
        dialog.exec()

    def start_puzzle_mode(self):
        """Start puzzle mode with difficulty selection."""
        from PyQt6.QtWidgets import QComboBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Puzzle Mode - Select Difficulty")
        dialog.setGeometry(200, 200, 400, 150)
        dialog.setStyleSheet("background-color: #2b2b2b; color: white;")
        
        layout = QVBoxLayout()
        
        label = QLabel("Select Puzzle Difficulty:")
        label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        layout.addWidget(label)
        
        difficulty_combo = QComboBox()
        difficulty_combo.addItems(["Easy (Mate in 1-2)", "Medium (Mate in 2-3)", "Hard (Mate in 3+)", "Random Tactical"])
        difficulty_combo.setStyleSheet("""
            QComboBox {
                background-color: #444;
                color: white;
                padding: 5px;
                border-radius: 4px;
            }
            QComboBox QAbstractItemView {
                background-color: #444;
                color: white;
            }
        """)
        layout.addWidget(difficulty_combo)
        
        btn_layout = QHBoxLayout()
        btn_start = QPushButton("Start Puzzle")
        btn_start.setStyleSheet("""
            QPushButton {
                background-color: #FF007F;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #FF0099; }
        """)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #cc0000;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #dd0000; }
        """)
        
        btn_layout.addWidget(btn_start)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)
        dialog.setLayout(layout)
        def on_start():
            difficulty = difficulty_combo.currentIndex()
            dialog.close()
            self.game_mode = "puzzle"
            self.puzzle_difficulty = difficulty  # 0=easy, 1=medium, 2=hard, 3=random
            self.puzzle_score = 0
            self.puzzle_solution_shown = False
            self.generate_puzzle()
            self.cleanup_timer()
            self.show_game()
            # Hide time display for puzzle mode
            if hasattr(self, 'white_time_label'):
                self.white_time_label.hide()
                self.black_time_label.hide()
            # make hint/solution buttons active
            self.update_puzzle_buttons()
            self.update_mode_buttons()
       
        
        btn_start.clicked.connect(on_start)
        btn_cancel.clicked.connect(dialog.close)
        dialog.exec()
    # ---------- puzzle helper buttons and logic ------------
    def show_puzzle_hint(self):
        """Display a hint (first move in the solution list)."""
        if self.puzzle_solution:
            # show SAN if available, otherwise fall back to UCI
            hint = (self.puzzle_solution_san[0]
                    if hasattr(self, 'puzzle_solution_san') and self.puzzle_solution_san
                    else self.puzzle_solution[0])
            QMessageBox.information(self, "Hint", f"Try this move: {hint}")

    def show_puzzle_solution(self):
        """Reveal the solution to the current puzzle."""
        if self.puzzle_solution and not self.puzzle_solution_shown:
            sols = (', '.join(self.puzzle_solution_san)
                    if hasattr(self, 'puzzle_solution_san')
                    else ', '.join(self.puzzle_solution))
            QMessageBox.information(self, "Solution", f"Solution: {sols}")
            self.puzzle_solution_shown = True

    def update_puzzle_buttons(self):
        # Hint/solution only exist in puzzle mode
        visible = (self.game_mode == "puzzle")
        self.btn_hint.setVisible(visible)
        self.btn_solution.setVisible(visible)

        enabled = visible and self.game_active and not self.game_over_flag
        self.btn_hint.setEnabled(enabled)
        self.btn_solution.setEnabled(enabled)
    def generate_puzzle(self):
        """Pick a puzzle and normalise the data.

        The old logic assumed the stored FEN position was the exact starting
        position for the solver.  Many datasets provide a FEN **before** the
        defender’s move, so the first element of the solution must be played by
        the engine first – the UI was never applying that move.
        """
        import random, chess

        # each entry may now be either a tuple (fen, [san list], name) or a
        # single string "fen | san1 san2 … | name" (the parser below handles both).
        puzzle_raw = [
            ("r1bqkb1r/pppp1ppp/2n2n2/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
             ["d4"], "Easy Puzzle 1"),
            # other puzzles omitted for brevity…
        ]

        def normalise(entry):
            if isinstance(entry, str):
                parts = [p.strip() for p in entry.split("|")]
                fen = parts[0]
                san = parts[1].split() if len(parts) > 1 else []
                name = parts[2] if len(parts) > 2 else ""
            else:
                fen, san, name = entry
            return fen, san, name

        def pick_from(list_of_puzzles):
            attempts = list_of_puzzles.copy()
            while attempts:
                fen, san_list, name = normalise(random.choice(attempts))
                board = chess.Board(fen)
                uci_list = []
                valid = True
                for san in san_list:
                    try:
                        move = board.parse_san(san)
                    except Exception:
                        valid = False
                        break
                    uci_list.append(move.uci())
                if not valid:
                    attempts.remove((fen, san_list, name))
                    continue
                # if the first move isn't legal assume it's opponent's move
                if uci_list and uci_list[0] not in {m.uci() for m in board.legal_moves}:
                    try:
                        board.push(chess.Move.from_uci(uci_list[0]))
                        uci_list = uci_list[1:]
                        san_list = san_list[1:]
                        fen = board.fen()
                    except Exception:
                        pass
                if valid:
                    return fen, uci_list, san_list, name
                attempts.remove((fen, san_list, name))
            # fallback
            fen, san_list, name = normalise(list_of_puzzles[0])
            board = chess.Board(fen)
            uci_list = []
            for s in san_list:
                try:
                    uci_list.append(board.parse_san(s).uci())
                except Exception:
                    pass
            return fen, uci_list, san_list, name

        # choose based on difficulty (identical logic to original)
        if self.puzzle_difficulty == 3:
            puzzle = pick_from(puzzle_raw)
        else:
            easy = puzzle_raw[:3]
            medium = puzzle_raw[3:4]
            hard = puzzle_raw[4:]
            if self.puzzle_difficulty == 0:
                puzzle = pick_from(easy)
            elif self.puzzle_difficulty == 1:
                puzzle = pick_from(medium)
            else:
                puzzle = pick_from(hard)

        if puzzle is None:
            QMessageBox.warning(self, "Puzzle Error", "No valid puzzles available.")
            return

        fen, uci_list, san_list, name = puzzle
        self.puzzle_fen = fen
        self.puzzle_solution = uci_list
        self.puzzle_solution_san = san_list
        self.puzzle_name = name
        # load the puzzle position
        self.game_state.board = chess.Board(self.puzzle_fen)
        self.puzzle_solution_shown = False
        self.board_widget.update()
        self.game_over_flag = False
        self.game_active = True
        self.ai_thinking = False
        self.board_widget.game_over = False
        self.board_widget.update()
        self.update_puzzle_buttons()
        if self.game_mode != "puzzle":
            self.update_engine_and_ui()
        print(f"\n{self.puzzle_name} loaded!")
        print(f"Solution (SAN): {', '.join(self.puzzle_solution_san)}")
        QMessageBox.information(self, "Puzzle Loaded", f"{self.puzzle_name}\n\nFind the best move!", QMessageBox.StandardButton.Ok)

    def start_game_review(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PGN File", "", "PGN Files (*.pgn);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    pgn_content = f.read()
                self._async_load_pgn(pgn_content, "review")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {e}")

    def reset_game(self):
        """Reset the board and start a new game."""
        # Update stockfish ELO for new game
        if self.game_mode == "computer":
            self.stockfish.set_elo(self.elo_strength)
        
        # Reset timers
        self.cleanup_timer()
        self.white_time = self.time_control
        self.black_time = self.time_control
        
        # Show time labels (might be hidden from review/training/puzzle mode)
        if hasattr(self, 'white_time_label'):
            if self.game_mode in ["computer", "local"]:
                self.white_time_label.show()
                self.black_time_label.show()
            else:
                self.white_time_label.hide()
                self.black_time_label.hide()
        
        self.update_time_display()
        
        # Reset board based on game mode
        if self.game_mode in ["review"]:
            pass  # Board already loaded from PGN
        elif self.game_mode == "opening_trainer":
            pass  # Board already loaded from PGN repertoire
        elif self.game_mode == "puzzle":
            # Puzzle board already loaded in generate_puzzle()
            import chess
            self.game_state.board = chess.Board(self.puzzle_fen)
        else:
            self.game_state.reset_board()
        
        self.game_over_flag = False
        self.game_result = None
        self.game_active = True
        self.ai_thinking = False
        self.board_widget.game_over = False
        self.board_widget.update()
        self.update_engine_and_ui()

        # update puzzle control buttons
        self.update_puzzle_buttons()
        self.update_mode_buttons()
        
        # Start the game timer (if applicable)
        if self.game_mode in ["computer", "local"]:
            self.game_timer = QTimer()
            self.game_timer.timeout.connect(self.decrement_time)
            self.game_timer.start(1000)  # Update every second

    def cleanup_timer(self):
        """Stop and clean up game timer."""
        if self.game_timer is not None:
            self.game_timer.stop()
            self.game_timer = None

    def decrement_time(self):
        """Decrement the active player's time."""
        if not self.game_active or self.game_over_flag or self.ai_thinking or self.time_control == 0:
            return
        
        if self.game_state.board.turn:  # White's turn
            self.white_time -= 1
            if self.white_time <= 0:
                self.white_time = 0
                self.handle_time_up(is_white=True)
        else:  # Black's turn
            self.black_time -= 1
            if self.black_time <= 0:
                self.black_time = 0
                self.handle_time_up(is_white=False)
        
        self.update_time_display()

    def handle_time_up(self, is_white):
        """Handle when a player's time runs out."""
        self.cleanup_timer()
        self.game_over_flag = True
        self.board_widget.game_over = True
        
        if is_white:
            self.game_result = "0-1"  # Black wins
            print("\nWhite's time is up - Black wins!")
        else:
            self.game_result = "1-0"  # White wins
            print("\nBlack's time is up - White wins!")
        
        self.board_widget.game_result = self.game_result
        self.board_widget.update()

    def update_time_display(self):
        """Update the time display labels."""
        # Handle "no time control" mode
        if self.time_control == 0:
            self.white_time_label.setText("∞")
            self.black_time_label.setText("∞")
            return
        
        white_mins = self.white_time // 60
        white_secs = self.white_time % 60
        black_mins = self.black_time // 60
        black_secs = self.black_time % 60
        
        white_color = "#E0E0E0" if self.game_state.board.turn else "#FFD700"
        black_color = "#333333" if not self.game_state.board.turn else "#FFD700"
        
        self.white_time_label.setStyleSheet(f"background-color: {white_color}; color: black; padding: 10px; font-weight: bold; font-size: 12px; border-radius: 5px;")
        self.black_time_label.setStyleSheet(f"background-color: {black_color}; color: white; padding: 10px; font-weight: bold; font-size: 12px; border-radius: 5px;")
        
        self.white_time_label.setText(f"White: {white_mins}:{white_secs:02d}")
        self.black_time_label.setText(f"Black: {black_mins}:{black_secs:02d}")

    def resign_game(self):
        """Current player resigns."""
        if self.game_over_flag or self.ai_thinking:
            return
        
        if self.game_state.board.turn:
            result = "0-1"  # White resigns, Black wins
            msg = "White Resigned - Black Wins!"
        else:
            result = "1-0"  # Black resigns, White wins
            msg = "Black Resigned - White Wins!"
        
        self.game_over_flag = True
        self.game_result = result
        self.board_widget.game_over = True
        self.board_widget.game_result = result
        self.board_widget.update()
        print(f"\n{msg}")

    def offer_draw(self):
        """Offer a draw."""
        if self.game_over_flag or self.ai_thinking:
            return
        
        if self.game_mode == "computer":
            # Auto-accept from stockfish
            self.game_over_flag = True
            self.game_result = "1/2-1/2"
            self.board_widget.game_over = True
            self.board_widget.game_result = "1/2-1/2"
            self.board_widget.update()
            print("\nGame ended in a draw by agreement!")
        else:
            # Local player mode - ask for confirmation
            reply = QMessageBox.question(self, "Draw Offer", "Accept draw offer?", 
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.game_over_flag = True
                self.game_result = "1/2-1/2"
                self.board_widget.game_over = True
                self.board_widget.game_result = "1/2-1/2"
                self.board_widget.update()
                print("\nGame ended in a draw by agreement!")

    # --- MOVE HANDLING ---
    def handle_user_move(self, uci_move):
        """Processes the human's move."""
        if self.game_over_flag or not self.game_active or self.ai_thinking:
            return
        
        # Mode-specific move validation
        if self.game_mode == "computer":
            # Can only move White pieces
            if not self.game_state.board.turn:
                return
        
        elif self.game_mode == "opening_trainer":
            # Player must play Black moves in response to White
            if self.game_state.board.turn:  # It's White's turn, play White move
                if self.game_state.make_move(uci_move):
                    self.board_widget.update()
                    self.update_engine_and_ui()
                    return
            else:  # Black's turn - player's move
                if self.game_state.make_move(uci_move):
                    self.training_score += 1
                    self.board_widget.update()
                    self.update_engine_and_ui()
                    # Auto-play White's next move
                    QTimer.singleShot(500, self.play_next_opening_move)
                    return
        
        elif self.game_mode == "puzzle":
            # Check if move is in solution
            if uci_move in self.puzzle_solution:
                # correct solution; play the move on board so user sees it
                self.game_state.make_move(uci_move)
                self.board_widget.update()
                # no need to calculate evaluation for puzzles
                self.puzzle_score += 1
                reply = QMessageBox.question(
                    self,
                    "Correct!",
                    "You found the solution!\n\nLoad another puzzle?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                )
                if reply == QMessageBox.StandardButton.Yes:
                    self.generate_puzzle()
                else:
                    # mark current puzzle finished so no further input is processed
                    self.game_over_flag = True
                return
            else:
                if not self.puzzle_solution_shown:
                    sols = (', '.join(self.puzzle_solution_san)
                            if hasattr(self, 'puzzle_solution_san')
                            else ', '.join(self.puzzle_solution))
                    reply = QMessageBox.warning(self, "Wrong Move", 
                        f"Wrong! The solution is: {sols}\n\nTry another puzzle?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    self.puzzle_solution_shown = True
                    if reply == QMessageBox.StandardButton.Yes:
                        self.generate_puzzle()
                    else:
                        self.game_over_flag = True
                    return
        
        elif self.game_mode == "local":
            # Both players can move
            pass
        
        elif self.game_mode == "review":
            # Allow move/variation creation
            if self.game_state.make_move(uci_move):
                self.review_positions = self.review_positions[:self.review_index + 1]
                self.review_positions.append(self.game_state.get_fen())
                self.review_index += 1
                self.board_widget.update()
                self.update_engine_and_ui()
            return
        
        # Attempt to make the move
        if self.game_state.make_move(uci_move):
            self.board_widget.update()
            self.update_engine_and_ui()
            self.update_time_display()
            
            if self.check_game_over():
                return
            
            # Trigger AI if needed
            if self.game_mode == "computer" and not self.game_state.board.turn:
                print(f"Human played: {uci_move}")
                print("Stockfish is thinking...")
                QTimer.singleShot(300, self.make_ai_move)
            elif self.game_mode == "local":
                print(f"Move played: {uci_move}")
    
    def play_next_opening_move(self):
        """Auto-play next move in opening trainer."""
        if self.game_state.board.turn:  # White's turn
            # Get next move from PGN (simulated - could be smarter)
            # For now, use Stockfish to suggest
            self.stockfish.set_fen_position(self.game_state.get_fen())
            best_move = self.stockfish.get_best_move()
            if best_move:
                if self.game_state.make_move(best_move):
                    self.board_widget.update()
                    self.update_engine_and_ui()
            if self.check_game_over():
                self.cleanup_timer()
                self.game_active = False

    def make_ai_move(self):
        """Make AI move on a separate thread."""
        if self.game_mode != "computer" or self.game_state.board.turn or self.game_over_flag:
            return
        
        self.ai_thinking = True
        current_fen = self.game_state.get_fen()
        
        # Create worker thread
        self.ai_worker = AIWorker(self.stockfish, current_fen)
        self.ai_thread = threading.Thread(target=self.ai_worker.run)
        self.ai_worker.move_ready.connect(self.on_ai_move_ready)
        self.ai_thread.daemon = True
        self.ai_thread.start()

    def on_ai_move_ready(self, best_move):
        """Handle AI move result."""
        if best_move and self.game_mode == "computer":
            print(f"Stockfish chose: {best_move}")
            self.game_state.make_move(best_move)
            self.board_widget.update()
            self.update_engine_and_ui()
            self.update_time_display()
            self.check_game_over()
        
        self.ai_thinking = False

    def update_engine_and_ui(self):
        """Queue a background evaluation unless we’re in puzzle mode."""
        if self.game_mode == "puzzle":
            self.eval_bar.update_eval({"type": "cp", "value": 0}, True)
            return

        current_fen = self.game_state.get_fen()
        is_white    = self.game_state.board.turn

        self.eval_worker = EvaluationWorker(self.stockfish, current_fen, is_white)
        self.eval_thread = threading.Thread(target=self.eval_worker.run)
        self.eval_worker.eval_ready.connect(self.on_eval_ready)
        self.eval_thread.daemon = True
        self.eval_thread.start()

    def on_eval_ready(self, eval_data, is_white_turn):
        """Slot called when EvaluationWorker emits a result."""
        self.eval_bar.update_eval(eval_data, is_white_turn)

    def _async_load_pgn(self, pgn_content, mode):
        self.pgn_loader = PGNLoader(self.game_state, pgn_content)
        self.pgn_thread = threading.Thread(target=self.pgn_loader.run)
        if mode == "opening_trainer":
            self.pgn_loader.finished.connect(self._on_opening_positions_loaded)
        else:  # review
            self.pgn_loader.finished.connect(self._on_review_positions_loaded)
        self.pgn_loader.error.connect(lambda e: QMessageBox.critical(self, "Error", f"Failed to load PGN: {e}"))
        self.pgn_thread.daemon = True
        self.pgn_thread.start()

    def _on_opening_positions_loaded(self, positions):
        if not positions:
            QMessageBox.warning(self, "Error", "Could not load PGN file.")
            return
        self.game_mode = "opening_trainer"
        self.training_score = 0
        self.training_mistakes = 0
        self.cleanup_timer()
        self.show_game()
        self.board_widget.update()
        self.update_engine_and_ui()
        self.white_time_label.hide(); self.black_time_label.hide()
        self.update_mode_buttons()
        print(f"\nLoaded Opening Repertoire with {len(positions)} positions")

    def _on_review_positions_loaded(self, positions):
        if not positions:
            QMessageBox.warning(self, "Error", "Could not load PGN file.")
            return
        self.review_positions = positions
        self.review_index     = 0
        self.game_mode        = "review"
        self.cleanup_timer()
        self.show_game()
        self.show_review_position()
        self.white_time_label.hide(); self.black_time_label.hide()
        self.update_mode_buttons()
        print(f"\nLoaded PGN with {len(positions)} positions")

    def show_review_position(self):
        fen = self.review_positions[self.review_index]
        self.game_state.board = chess.Board(fen)
        self.board_widget.update()
        self.update_engine_and_ui()

    def review_next(self):
        if self.review_index < len(self.review_positions) - 1:
            self.review_index += 1
            self.show_review_position()

    def review_prev(self):
        if self.review_index > 0:
            self.review_index -= 1
            self.show_review_position()

    def update_mode_buttons(self):
        """Show/hide controls that are only relevant in certain modes."""
        self.btn_hint.setVisible(self.game_mode == "puzzle")
        self.btn_solution.setVisible(self.game_mode == "puzzle")
        self.btn_prev.setVisible(self.game_mode == "review")
        self.btn_next.setVisible(self.game_mode == "review")

    def check_game_over(self):
        """Check if the game is over."""
        if self.game_state.is_game_over():
            result = self.game_state.get_result()
            self.game_over_flag = True
            self.game_result = result
            self.board_widget.game_over = True
            self.board_widget.game_result = result
            self.board_widget.update()
            
            if result == "1-0":
                print("\nWhite Wins by Checkmate!")
            elif result == "0-1":
                print("\nBlack Wins by Checkmate!")
            else:
                print("\nGame Over - Draw!")
            
            return True
        return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChessAppMain()
    window.show()
    sys.exit(app.exec())