import chess
import chess.pgn
import io

class GameState:
    def __init__(self):
        # Initialize a standard chess board starting position
        self.board = chess.Board()

    def make_move(self, uci_move: str) -> bool:
        """
        Attempts to make a move using Universal Chess Interface (UCI) format (e.g., 'e2e4').
        Returns True if the move is legal and was made, False otherwise.
        """
        try:
            move = chess.Move.from_uci(uci_move)
            if move in self.board.legal_moves:
                self.board.push(move)
                return True
            return False
        except ValueError:
            # Catches poorly formatted strings
            return False

    def get_legal_moves(self) -> list:
        """Returns a list of all legal moves for the current position in UCI format."""
        return [move.uci() for move in self.board.legal_moves]

    def reset_board(self):
        """Resets the board to the standard starting position."""
        self.board.reset()

    def load_pgn(self, pgn_string: str) -> list:
        """
        Loads a game from a PGN string. 
        Returns a list of board positions (FEN strings) for the review feature.
        """
        positions = []
        try:
            pgn_io = io.StringIO(pgn_string)
            game = chess.pgn.read_game(pgn_io)
            if game is None:
                return []
            
            # Replay the game from the beginning to grab every position
            board = game.board()
            positions.append(board.fen())
            for move in game.mainline_moves():
                board.push(move)
                positions.append(board.fen())
                
            self.board = board # Set current state to the end of the PGN
            return positions
        except Exception as e:
            print(f"Error loading PGN: {e}")
            return []

    def get_fen(self) -> str:
        """Returns the current board state in FEN (Forsyth-Edwards Notation)."""
        return self.board.fen()

    def is_game_over(self) -> bool:
        """Checks if the game has ended (checkmate, stalemate, draw)."""
        return self.board.is_game_over()
    
    def get_result(self) -> str:
        """Returns the result of the game ('1-0', '0-1', '1/2-1/2', or '*')."""
        return self.board.result()