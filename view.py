from tile import TileColor, Tile
import sys

def render_title():
    title = [
        Tile("W", TileColor.UNKNOWN, True),
        Tile("O", TileColor.EXACTMATCH, True),
        Tile("R", TileColor.CONTAIN, True),
        Tile("D", TileColor.NOMATCH, True),
        Tile("L", TileColor.CONTAIN, True),
        Tile("E", TileColor.UNKNOWN, True),
    ]
    lines = [" ".join(tile.lines[i] for tile in title) for i in range(3)]
    return [f"\x1b[40G{line}" for line in lines]
    
def render_help():
    return "\n\x1b[8Cctrl+c - quit\x1b[4Center - submit word\x1b[4Cbackspace - remove last"

def render_board():
    board = []
    for _ in range(6):
        tiles = [Tile(bold=True) for _ in range(5)]
        lines = [" ".join(tile.lines[i] for tile in tiles) for i in range(3)]
        board += lines
    return board

def render_keyboard():
    rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    keyboard = []
    for row in rows:
        keys = [Tile(char, TileColor.UNKNOWN, True) for char in row]
        lines = [" ".join(tile.lines[i] for tile in keys) for i in range(3)]
        keyboard += lines
    return keyboard

def render_frame():
    frame = ""
    board = render_board()
    title = render_title()
    keyboard = render_keyboard()
    for i in range(len(board)):
        frame += board[i] if i < len(board) else ""
        frame += title[i - 1] if i < len(title) + 1 and i != 0 else ""
        frame += keyboard[i - 5] if i < len(keyboard) + 5 and i > 4 else ""
        frame += "\n"
    frame += render_help()
    return frame

if __name__ == "__main__":
    sys.stdout.write("\x1b[2J\x1b[1;1H") # clear screen, pindah cursor ke (1,1)
    sys.stdout.write(render_frame())
    sys.stdout.flush()