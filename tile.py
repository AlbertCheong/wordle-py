class TileColor :
    UNKNOWN    = (211, 214, 218) # 0xD3D6DA
    NOMATCH    = (120, 124, 126) # 0x787C7E
    CONTAIN    = (201, 179,  88) # 0xC9B358
    EXACTMATCH = (105, 170, 100) # 0x69AA64

class Tile:
    def __init__(self, char=" ", color=TileColor.UNKNOWN, bold=False):
        self.char  = char
        self.color = color
        self.bold  = bold
        self.lines = []
        self.view()
    
    def set_char(self, char):
        self.char = char
        self.view()
        return self

    def set_color(self, color):
        self.color = color
        self.view()
        return self
    
    def set_bold(self, bold):
        self.bold = bold
        self.view()
        return self

    def view(self):
        R, G, B = self.color
        # '\x1b[38;2;R;G;Bm': untuk mengatur warna teks ke RGB(R,G,B).
        # '\x1b[1m'         : untuk mengatur teks menjadi bold.
        color = f"\x1b[38;2;{R};{G};{B}m"
        bold  = "\x1b[1m" if self.bold else ""
        self.lines = [
            f"{color}{bold}╭───╮\x1b[0m",
            f"{color}{bold}│ {self.char.upper()} │\x1b[0m",
            f"{color}{bold}╰───╯\x1b[0m",
        ]
    
    def string(self):
        return "\n".join(self.lines)

    def is_empty(self):
        return self.char == " "

if __name__ == "__main__":
    tile = Tile()
    print(tile.string())
    
    tile                                 \
        .set_char("A")                   \
        .set_color(TileColor.EXACTMATCH) \
        .set_bold(True)
    
    print(tile.string())