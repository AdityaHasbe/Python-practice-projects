import os
import platform
from stockfish import Stockfish

class StockfishHandler:
    def __init__(self, elo=1500, depth=15):
        """
        Initializes the Stockfish engine. We dynamically build the path to the 
        executable so it works regardless of where you run the main script from.
        """
        # Get the absolute path of the directory two levels up (the chess_app root)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Automatically handle the .exe extension for Windows vs Mac/Linux
        exec_name = "stockfish.exe" if platform.system() == "Windows" else "stockfish"
        self.stockfish_path = os.path.join(base_dir, "assets", exec_name)
        
        try:
            # We initialize Stockfish and turn on the Elo limiter so it doesn't always play like a Grandmaster
            self.engine = Stockfish(
                path=self.stockfish_path, 
                depth=depth, 
                parameters={"UCI_LimitStrength": True, "UCI_Elo": elo}
            )
        except Exception as e:
            print(f"CRITICAL ERROR: Could not load Stockfish from {self.stockfish_path}")
            print("Did you place the executable in the exact folder and rename it to 'stockfish.exe'?")
            print(f"Error details: {e}")
            self.engine = None

    def set_fen_position(self, fen: str):
        """Updates the engine's internal board state to match our game."""
        if self.engine:
            self.engine.set_fen_position(fen)

    def get_best_move(self) -> str:
        """Asks Stockfish for the absolute best move in the current position."""
        if self.engine:
            return self.engine.get_best_move()
        return None

    def get_evaluation(self) -> dict:
        """
        Returns the evaluation of the position. 
        Format: {"type": "cp", "value": 12} (centipawns) 
        or {"type": "mate", "value": -3} (mate in 3)

        The underlying stockfish library will emit a UserWarning when the
        strength limiter is in use reminding the caller that the evaluation
        always reflects the full-strength engine.  We suppress that message so
        it doesn't flood the log.
        """
        if self.engine:
            import warnings
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message="Note that even though you've set Stockfish to play on a weaker elo or skill level, get_evaluation will still return full strength Stockfish's evaluation of the position."
                )
                return self.engine.get_evaluation()
        return {"type": "cp", "value": 0}

    def set_elo(self, elo: int):
        """Adjusts the difficulty of the engine on the fly.

        Stockfish requires a minimum of 1320 when the strength limiter is
        enabled.  If the caller passes a lower value we clamp it silently
        so that the UI doesn't crash with a ValueError.
        """
        if not self.engine:
            return

        # enforce minimum allowed elo
        if elo < 1320:
            elo = 1320
        try:
            self.engine.update_engine_parameters({"UCI_LimitStrength": True, "UCI_Elo": elo})
        except ValueError as ve:
            # should not happen thanks to the clamp above but log just in case
            print(f"Warning: unable to set elo {elo} ({ve})")