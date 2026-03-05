import os
import chess
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPolygonF
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal

class BoardWidget(QWidget):
    # This signal tells the main window when a user tries to make a move
    move_requested = pyqtSignal(str) 

    def __init__(self, game_state):
        super().__init__()
        self.game_state = game_state
        self.square_size = 60
        self.setMinimumSize(480, 480)  # 8x60

        # Drag and drop state variables
        self.dragging = False
        self.drag_start_square = None
        self.drag_current_pos = None
        self.drag_piece = None
        
        # Game over state
        self.game_over = False
        self.game_result = None

        self.piece_renderers = self.load_piece_graphics()

    def load_piece_graphics(self):
        """Loads SVG files from the assets/pieces directory."""
        renderers = {}
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pieces_dir = os.path.join(base_dir, "assets", "pieces")

        # Map python-chess piece symbols to our file names
        piece_map = {
            'P': 'wp', 'N': 'wn', 'B': 'wb', 'R': 'wr', 'Q': 'wq', 'K': 'wk',
            'p': 'bp', 'n': 'bn', 'b': 'bb', 'r': 'br', 'q': 'bq', 'k': 'bk'
        }

        for symbol, filename in piece_map.items():
            path = os.path.join(pieces_dir, f"{filename}.svg")
            if os.path.exists(path):
                renderers[symbol] = QSvgRenderer(path)
            else:
                print(f"Warning: Missing piece graphic at {path}")
        return renderers

    def get_square_from_pos(self, pos):
        """Converts an x,y screen pixel coordinate into a chess square index (0-63)."""
        col = int(pos.x() // self.square_size)
        row = int(pos.y() // self.square_size)
        
        # Ensure clicks outside the board don't crash
        if col < 0 or col > 7 or row < 0 or row > 7:
            return None
            
        # PyQt coordinates are top-left (0,0), chess is bottom-left (a1=0, a8=56)
        # We must flip the row to match chess logic
        return chess.square(col, 7 - row)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.game_over:
            square = self.get_square_from_pos(event.pos())
            if square is not None:
                piece = self.game_state.board.piece_at(square)
                if piece:
                    self.dragging = True
                    self.drag_start_square = square
                    self.drag_piece = piece
                    self.drag_current_pos = event.pos()
                    self.update()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.drag_current_pos = event.pos()
            # Update only the region where the piece is being dragged (optimization)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.dragging:
            self.dragging = False
            drop_square = self.get_square_from_pos(event.pos())
            
            if drop_square is not None and drop_square != self.drag_start_square:
                # Convert square indices to a UCI string (e.g., 'e2e4')
                move_uci = chess.square_name(self.drag_start_square) + chess.square_name(drop_square)
                
                # Check for pawn promotion (auto-promote to queen for simplicity right now)
                if self.drag_piece.piece_type == chess.PAWN:
                    if (self.drag_piece.color == chess.WHITE and chess.square_rank(drop_square) == 7) or \
                       (self.drag_piece.color == chess.BLACK and chess.square_rank(drop_square) == 0):
                        move_uci += "q"

                # Send the attempted move out to the main application logic
                self.move_requested.emit(move_uci)

            self.drag_piece = None
            self.drag_start_square = None
            self.update() # Snap pieces back or finalize move visually

    def get_winning_king_square(self):
        """Returns the square of the winning king if game is over."""
        if not self.game_over or not self.game_result:
            return None
        
        # Find the king of the winning side
        if self.game_result == "1-0":  # White wins
            return self.game_state.board.king(chess.WHITE)
        elif self.game_result == "0-1":  # Black wins
            return self.game_state.board.king(chess.BLACK)
        
        return None

    def paintEvent(self, event):
        """Optimized rendering - only draw what's needed."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # Calculate board size based on widget size
        board_size = min(self.width(), self.height())
        self.square_size = board_size / 8
        
        # Draw board - optimize by drawing only affected region
        colors = [QColor("#eeeed2"), QColor("#769656")]
        for row in range(8):
            for col in range(8):
                is_dark = (row + col) % 2 == 1
                x = col * self.square_size
                y = row * self.square_size
                painter.fillRect(int(x), int(y), int(self.square_size), int(self.square_size), colors[is_dark])

        # Draw pieces - cache check to avoid redundant renders
        for square in chess.SQUARES:
            if self.dragging and square == self.drag_start_square:
                continue
            
            piece = self.game_state.board.piece_at(square)
            if piece and piece.symbol() in self.piece_renderers:
                col = chess.square_file(square)
                row = 7 - chess.square_rank(square)
                x = col * self.square_size
                y = row * self.square_size
                rect = QRectF(x, y, self.square_size, self.square_size)
                self.piece_renderers[piece.symbol()].render(painter, rect)

        # Draw dragged piece
        if self.dragging and self.drag_piece and self.drag_piece.symbol() in self.piece_renderers:
            x = self.drag_current_pos.x() - self.square_size / 2
            y = self.drag_current_pos.y() - self.square_size / 2
            rect = QRectF(x, y, self.square_size, self.square_size)
            self.piece_renderers[self.drag_piece.symbol()].render(painter, rect)
        
        # Draw crown on winning king
        if self.game_over and self.game_result in ["1-0", "0-1"]:
            winning_square = self.get_winning_king_square()
            if winning_square is not None:
                col = chess.square_file(winning_square)
                row = 7 - chess.square_rank(winning_square)
                self.draw_crown(painter, col * self.square_size, row * self.square_size)

    def draw_crown(self, painter, x, y):
        """Draw a golden crown in the top-right corner of the king's square."""
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Crown dimensions - smaller and positioned in corner
        crown_size = self.square_size * 0.35
        # Position in top-right corner of the square
        start_x = x + self.square_size - crown_size - 5
        start_y = y + 5
        
        # Draw golden crown
        gold = QColor("#FFD700")
        outline = QColor("#FFA500")
        
        painter.setBrush(QBrush(gold))
        painter.setPen(QPen(outline, 2))
        
        # Crown shape: base rectangle with 3 peaks
        crown_height = crown_size * 0.6
        base_width = crown_size
        base_height = crown_size * 0.3
        
        # Draw base
        painter.drawRect(int(start_x), int(start_y + crown_height - base_height), 
                        int(base_width), int(base_height))
        
        # Draw 3 peaks
        peak_width = base_width / 4
        for i in range(3):
            peak_x = start_x + (i + 0.5) * (base_width / 3) - peak_width / 2
            peak_y = start_y
            points = [
                (peak_x, peak_y + crown_height),
                (peak_x + peak_width / 2, peak_y),
                (peak_x + peak_width, peak_y + crown_height)
            ]
            
            polygon = QPolygonF([QPointF(p[0], p[1]) for p in points])
            painter.drawPolygon(polygon)
        
        painter.restore()