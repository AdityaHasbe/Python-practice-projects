from PyQt6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel
from PyQt6.QtCore import Qt

class EvaluationBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(60) 
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        self.eval_label = QLabel("0.00")
        self.eval_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.eval_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")

        self.bar = QProgressBar()
        self.bar.setOrientation(Qt.Orientation.Vertical)
        self.bar.setMinimum(0)
        self.bar.setMaximum(100)
        self.bar.setValue(50) 
        self.bar.setTextVisible(False) 
        
        self.bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #555555;
                border-radius: 5px;
                background-color: #333333; 
            }
            QProgressBar::chunk {
                background-color: #E0E0E0; 
                border-radius: 3px;
            }
        """)

        layout.addWidget(self.eval_label)
        layout.addWidget(self.bar)
        self.setLayout(layout)

    def update_eval(self, eval_data, is_white_turn):
        """
        Translates Stockfish's mathematical output into visuals, 
        accounting for whose turn it currently is.
        """
        if eval_data['type'] == 'mate':
            mate_in = eval_data['value']
            
            # Flip mate score if it is Black's turn looking at a White mate
            if not is_white_turn:
                mate_in = -mate_in
                
            if mate_in > 0:
                self.eval_label.setText(f"M{mate_in}")
                self.bar.setValue(100) 
            else:
                self.eval_label.setText(f"-M{abs(mate_in)}")
                self.bar.setValue(0) 
        else:
            score = eval_data['value'] / 100.0
            
            # STOCKFISH QUIRK FIX: Flip the score if it is Black's turn
            # so the bar always reflects the absolute position for White.
            if not is_white_turn:
                score = -score
            
            if score > 0:
                self.eval_label.setText(f"+{score:.2f}")
            elif score < 0:
                self.eval_label.setText(f"{score:.2f}")
            else:
                self.eval_label.setText("0.00")

            # Increased sensitivity (x15 instead of x10) so early moves are visible
            win_chance = 50 + (score * 15) 
            win_chance = max(0, min(100, win_chance))
            self.bar.setValue(int(win_chance))