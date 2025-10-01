import sys
import msvcrt

UNKNOWN = (211, 214, 218) # 0xD3D6DA
NOMATCH = (120, 124, 126) # 0x787C7E
CONTAIN = (201, 179,  88) # 0xC9B358
EXACTMATCH = (105, 170, 100) # 0x69AA64

class Tile:
    def __init__(self, char="_", color=UNKNOWN):
        self.char  = char
        self.color = color
        self.lines = []
        self.update()

    def __str__(self):
        return "\n".join(self.lines)
    
    def set_char(self, char):
        self.char = char
        self.update()

    def set_color(self, color):
        self.color = color
        self.update()

    def update(self):
        R, G, B = self.color
        color = f"\033[38;2;{R};{G};{B}m"
        self.lines = [
            f"{color}\033[1m╭───╮\033[0m",
            f"{color}\033[1m│ {self.char.upper()} │\033[0m",
            f"{color}\033[1m╰───╯\033[0m",
        ]

    def is_empty(self):
        return self.char == "_"

class Board:
    def __init__(self, size=5):
        self.tiles = [Tile() for _ in range(size)]

    def place(self, char):
        for tile in self.tiles:
            if tile.is_empty():
                tile.set_char(char)
                return

    def is_full(self):
        return all(not t.is_empty() for t in self.tiles)

def join_horizontal(tiles):
    return "\n".join(" ".join(tile.lines[i] for tile in tiles) for i in range(3))

def join_vertical(tiles):
    return "\n".join(str(tile) for tile in tiles) + "\n"

def get_key_pressed():
    if msvcrt.kbhit():
        return msvcrt.getch()
    return None

class Program:
    def __init__(self):
        self.board = Board(size=5)
        self.running = True

    def draw_frame(self, prev_frame, curr_frame):
        for r, (pline, cline) in enumerate(zip(prev_frame, curr_frame)):
            if pline != cline:
                sys.stdout.write(f"\033[{r+1};1H{cline}")
        sys.stdout.flush()

    def run(self):
        # clear screen, sembunyikan cursor dan lgsg flush dari stdout.
        sys.stdout.write("\033[2J\033[H\033[?25l")
        sys.stdout.flush()

        prev_frame = [""] * 4
        try:
            while self.running:
                key = get_key_pressed()
                if not key is None:
                    if key == b'\x1b':
                        self.running = False
                    elif key.isalpha():
                        self.board.place(key.decode("utf-8"))

                    if self.board.is_full():
                        self.running = False

                board_str = join_horizontal(self.board.tiles)
                curr_frame = board_str.split("\n") + ["Type a letter (ESC to quit): "]

                self.draw_frame(prev_frame, curr_frame)
                prev_frame = curr_frame
        finally:
            sys.stdout.write("\033[?25h\n")
            sys.stdout.flush()

program = Program()
program.run()
