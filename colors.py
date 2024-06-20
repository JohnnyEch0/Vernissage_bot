class hex_color_scheme:
    def __init__(self, hex_color):
        self.hex_color = hex_color
        self.r = int(hex_color[1:3], 16)
        self.g = int(hex_color[3:5], 16)
        self.b = int(hex_color[5:7], 16)
    
    def __str__(self):
        return self.hex_color
    
    def darker(self, factor=0.8):
        self.r = int(self.r * factor)
        self.g = int(self.g * factor)
        self.b = int(self.b * factor)
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    def desaturate(self, factor=0.8):
        self.r = int(self.r * factor + 255 * (1 - factor))
        self.g = int(self.g * factor + 255 * (1 - factor))
        self.b = int(self.b * factor + 255 * (1 - factor))
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    def __repr__(self) -> str:
        return self.hex_color
    


    
