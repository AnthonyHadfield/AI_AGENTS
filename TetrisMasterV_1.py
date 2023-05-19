import tkinter as tk
import random

# Constants
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 460
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 20
piece_colors = {
    "I": "cyan",
    "J": "blue",
    "L": "orange",
    "O": "yellow",
    "S": "green",
    "T": "purple",
    "Z": "red"
}

class TetrisGame:
    def __init__(self):
        self.master = tk.Tk()
        self.canvas_width = BOARD_WIDTH * CELL_SIZE
        self.canvas_height = BOARD_HEIGHT * CELL_SIZE
        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg='light gray')
        self.canvas.pack(padx=20, pady=20)

        self.board = [[""] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_piece = None
        self.current_piece_coords = {"row": 0, "column": 0}

        self.master.bind('<Down>', self.move_down)

        self.tetris_window()  # Create the game window
        self.create_piece()  # Create the initial piece
        self.update()  # Start the game loop

    def tetris_window(self):
        window_width = 300
        window_height = 445

        canvas_width = window_width - 40  # Subtract padding
        canvas_height = window_height - 40  # Subtract padding

        self.canvas.config(width=canvas_width, height=canvas_height)

        self.master.title("Tetris Game")
        self.master.geometry(f"{window_width}x{window_height}")

    def create_piece(self):
        pieces = ["I", "J", "L", "O", "S", "T", "Z"]
        piece_type = random.choice(pieces)
        piece_color = piece_colors[piece_type]
        piece = []
        if piece_type == "I":
            piece = [[1, 1, 1, 1]]
        elif piece_type == "J":
            piece = [[1, 0, 0], [1, 1, 1]]
        elif piece_type == "L":
            piece = [[0, 0, 1], [1, 1, 1]]
        elif piece_type == "O":
            piece = [[1, 1], [1, 1]]
        elif piece_type == "S":
            piece = [[0, 1, 1], [1, 1, 0]]
        elif piece_type == "T":
            piece = [[0, 1, 0], [1, 1, 1]]
        elif piece_type == "Z":
            piece = [[1, 1, 0], [0, 1, 1]]

        # Adjust initial position if it causes collision
        initial_row = 0
        initial_col = BOARD_WIDTH // 2 - len(piece[0]) // 2
        if not self.is_valid_position({
            "piece": piece,
            "type": piece_type,
            "color": piece_color,
            "row": initial_row,
            "column": initial_col
        }):
            initial_row += 1

        self.current_piece = {
            "piece": piece,
            "type": piece_type,
            "color": piece_color,
            "row": initial_row,
            "column": initial_col
        }

    def is_valid_position(self, piece):
        for i in range(len(piece["piece"])):
            for j in range(len(piece["piece"][0])):
                if (
                    piece["piece"][i][j] == 1
                    and (
                        piece["row"] + i >= BOARD_HEIGHT
                        or piece["column"] + j < 0
                        or piece["column"] + j >= BOARD_WIDTH
                        or self.board[piece["row"] + i][piece["column"] + j] != ""
                    )
                ):
                    return False
        return True

    def draw_piece(self, piece):
        for i in range(len(piece["piece"])):
            for j in range(len(piece["piece"][0])):
                if piece["piece"][i][j] == 1:
                    x = piece["column"] * CELL_SIZE + j * CELL_SIZE
                    y = piece["row"] * CELL_SIZE + i * CELL_SIZE
                    self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=piece["color"])

    def draw_board(self):
        self.canvas.delete("board")
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if self.board[row][col] != "":
                    x1 = col * CELL_SIZE
                    y1 = row * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=self.board[row][col], tags="board"
                    )

    def update(self):
        self.canvas.delete("all")
        self.draw_board()
        self.draw_piece(self.current_piece)
        self.move_down()

        self.master.after(500, self.update)

    def move_down(self, event=None):
        if self.is_valid_position(
            {
                "piece": self.current_piece["piece"],
                "type": self.current_piece["type"],
                "color": self.current_piece["color"],
                "row": self.current_piece["row"] + 1,
                "column": self.current_piece["column"],
            }
        ):
            self.current_piece["row"] += 1
        else:
            # Add current piece to the board
            for i in range(len(self.current_piece["piece"])):
                for j in range(len(self.current_piece["piece"][0])):
                    if self.current_piece["piece"][i][j] == 1:
                        self.board[
                            self.current_piece["row"] + i
                        ][self.current_piece["column"] + j] = self.current_piece["color"]

            self.create_piece()

if __name__ == "__main__":
    game = TetrisGame()
    game.master.mainloop()