# import sys
# import msvcrt

# UNKNOWN = (211, 214, 218) # 0xD3D6DA
# NOMATCH = (120, 124, 126) # 0x787C7E
# CONTAIN = (201, 179,  88) # 0xC9B358
# EXACTMATCH = (105, 170, 100) # 0x69AA64

# class Tile:
#     def __init__(self, char="_", color=UNKNOWN):
#         self.char  = char
#         self.color = color
#         self.lines = []
#         self.update()

#     def __str__(self):
#         return "\n".join(self.lines)
    
#     def set_char(self, char):
#         self.char = char
#         self.update()

#     def set_color(self, color):
#         self.color = color
#         self.update()

#     def update(self):
#         R, G, B = self.color
#         # '\x1b[38;2;R;G;Bm': untuk mengatur warna teks ke RGB(R,G,B).
#         # '\x1b[1m'         : untuk mengatur teks menjadi bold.
#         color = f"\x1b[38;2;{R};{G};{B}m"
#         self.lines = [
#             f"{color}\x1b[1m╭───╮\x1b[0m",
#             f"{color}\x1b[1m│ {self.char.upper()} │\x1b[0m",
#             f"{color}\x1b[1m╰───╯\x1b[0m",
#         ]

#     def is_empty(self):
#         return self.char == "_"

# class Board:
#     def __init__(self, size=5):
#         self.tiles = [Tile() for _ in range(size)]

#     def place(self, char):
#         for tile in self.tiles:
#             if tile.is_empty():
#                 tile.set_char(char)
#                 return

#     def is_full(self):
#         return all(not t.is_empty() for t in self.tiles)

# def join_horizontal(tiles):
#     return "\n".join(" ".join(tile.lines[i] for tile in tiles) for i in range(3))

# def join_vertical(tiles):
#     return "\n".join(str(tile) for tile in tiles) + "\n"

# def get_key_pressed():
#     # msvcrt.kbhit(): mengecek apakah ada tombol yang ditekan.
#     # msvcrt.getch(): membaca karakter yang ditekan.
#     if msvcrt.kbhit():
#         return msvcrt.getch()
#     return None

# class Program:
#     def __init__(self):
#         self.board = Board(size=5)
#         self.running = True

#     def draw_frame(self, frame):
#         for r, line in enumerate(frame):
#             # pindah cursor ke baris ke-r+1, kolom ke-1
#             # dan cetak line.
#             sys.stdout.write(f"\x1b[{r+1};1H{line}")
#         sys.stdout.flush()

#     def run(self):
#         # '[2J'  : clear screen.
#         # '[1;1H': pindah cursor ke posisi (1,1).
#         # '[?25l': hide cursor pada screen.
#         sys.stdout.write("\x1b[2J\x1b[1;1H\x1b[?25l")
#         sys.stdout.flush()

#         try:
#             while self.running:
#                 key = get_key_pressed()
#                 if not key is None:
#                     # b'\x1b': kode ASCII untuk tombol ESC.
#                     if key == b'\x1b':
#                         self.running = False
#                     elif key.isalpha():
#                         self.board.place(key.decode("utf-8"))

#                     if self.board.is_full():
#                         self.running = False

#                 board_str = join_horizontal(self.board.tiles)
#                 curr_frame = board_str.split("\n") + ["Type a letter (ESC to quit): "]
#                 self.draw_frame(curr_frame)
#         finally:
#             # pastikan mengembalikan kondisi awal terminal
#             # dan flush output tersisa di stdout.
#             # '[?25h' : unhide cursor pada screen.
#             sys.stdout.write("\x1b[?25h\n")
#             sys.stdout.flush() # dapat di-ignore karena stdout akan selalu di-flush saat program berakhir.

# # driver code
# program = Program()
# program.run()

import msvcrt, time

class Text :

    def __init__(self, size=5):
        self.contains = [" " for _ in range(size)]
        self.selected = 0
        self.size = size

    def is_full(self) -> bool:
        return all([x != " " for x in self.contains])
    
    def is_empty(self) -> bool:
        return self.selected == 0

    def update(self, key: str) -> None:
        if key:
            if key.isalpha() and not self.is_full():
                self.contains[self.selected] = key.upper()
                self.selected += 1

            elif key == "\r":
                self.contains = [" " for _ in range(self.size)]
                self.selected = 0

            elif key == "\x08" and not self.is_empty():
                self.selected -= 1
                self.contains[self.selected] = " "

            else:
                pass

    def string(self) -> str:
        line = [
            c if i != self.selected else "_"      \
            if c == " " else c                    \
            for i, c in enumerate(self.contains)
        ]
        return ''.join(line)

def get_key():
    if msvcrt.kbhit():
        ch = msvcrt.getch() 
        if ch in {b'\x00', b'\xe0'}:
            _  = msvcrt.getch()
            return None
        return ch.decode("utf-8")
    return None

print("\x1b[?25l", end="")

text = Text()
try :
    while 1:
        line = text.string()
        text.update(get_key())
        print(f"[{line}]\r", end="")
        time.sleep(0.01)
finally:
    print("\x1b[?25h", end="")