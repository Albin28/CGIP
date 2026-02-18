import tkinter as tk
import datetime

# --- Constants ---
WIDTH, HEIGHT = 800, 800
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

# Dot Matrix (5x7) & Layout
DOT_SIZE = 6
DOT_GAP = 2
MATRIX_W, MATRIX_H = 5, 7
DIGIT_W = MATRIX_W * (DOT_SIZE + DOT_GAP) - DOT_GAP
DIGIT_SPACING = 10
SECTION_SPACING = 20
COLON_W = DOT_SIZE

# Circles
RADII = {'H': 300, 'M': 280, 'S': 260}
WIDTH_CIRCLE = 10
COLORS = {'H': ("#00FF00", "#112211"), 'M': ("#0000FF", "#111122"), 'S': ("#FF0000", "#221111")}

# Digit Patterns (1=ON, 0=OFF) - Compact & Understandable
# Each sub-list represents a row of 5 dots.
DIGIT_PATTERNS = {
    0: [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,1,1], [1,0,1,0,1], [1,1,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
    1: [[0,0,1,0,0], [0,1,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,1,1,1,0]],
    2: [[0,1,1,1,0], [1,0,0,0,1], [0,0,0,0,1], [0,0,0,1,0], [0,0,1,0,0], [0,1,0,0,0], [1,1,1,1,1]],
    3: [[0,1,1,1,0], [1,0,0,0,1], [0,0,0,0,1], [0,0,1,1,0], [0,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
    4: [[0,0,0,1,0], [0,0,1,1,0], [0,1,0,1,0], [1,0,0,1,0], [1,1,1,1,1], [0,0,0,1,0], [0,0,0,1,0]],
    5: [[1,1,1,1,1], [1,0,0,0,0], [1,1,1,1,0], [0,0,0,0,1], [0,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
    6: [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,0], [1,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
    7: [[1,1,1,1,1], [0,0,0,0,1], [0,0,0,1,0], [0,0,1,0,0], [0,1,0,0,0], [0,1,0,0,0], [0,1,0,0,0]],
    8: [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
    9: [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,1], [0,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
}

class DigitalClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock (IST) - Dot Matrix")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
        self.canvas.pack()
        self.update_clock()

    def get_ist_time(self):
        return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5, minutes=30)

    def draw_dots(self, x, y, matrix, color="#00FF00"):
        """Draws a grid of dots based on the provided matrix (list of lists)."""
        for r, row in enumerate(matrix):
            for c, val in enumerate(row):
                if val:
                    px, py = x + c * (DOT_SIZE + DOT_GAP), y + r * (DOT_SIZE + DOT_GAP)
                    self.canvas.create_rectangle(px, py, px + DOT_SIZE, py + DOT_SIZE, fill=color, outline="")

    def draw_digit_pair(self, x, y, value):
        """Helper to draw two digits (e.g., '12' from 12). Returns new X position."""
        self.draw_dots(x, y, DIGIT_PATTERNS[value // 10])
        x += DIGIT_W + DIGIT_SPACING
        self.draw_dots(x, y, DIGIT_PATTERNS[value % 10])
        return x + DIGIT_W + SECTION_SPACING

    def draw_circle(self, radius, count, value, colors, width=10):
        """Draws a segmented circle."""
        angle, gap = 360 / count, 1
        for i in range(count):
            start = 90 - (i + 1) * angle + gap / 2
            color = colors[0] if i < value else colors[1]
            self.canvas.create_arc(CENTER_X - radius, CENTER_Y - radius, CENTER_X + radius, CENTER_Y + radius,
                                   start=start, extent=angle - gap, width=width, style=tk.ARC, outline=color)

    def update_clock(self):
        now = self.get_ist_time()
        self.canvas.delete("all")
        
        # 1. Draw Circles
        self.draw_circle(RADII['H'], 24, now.hour, COLORS['H'])
        self.draw_circle(RADII['M'], 60, now.minute, COLORS['M'])
        self.draw_circle(RADII['S'], 60, now.second, COLORS['S'])

        # 2. Draw Digital Time (Centered)
        # Calculate start X to center the display: 6 digits + 2 colons + spacing
        grp_w = 2 * DIGIT_W + DIGIT_SPACING
        total_w = 3 * grp_w + 2 * (SECTION_SPACING + COLON_W + SECTION_SPACING)
        x = CENTER_X - total_w // 2
        y = CENTER_Y - (MATRIX_H * (DOT_SIZE + DOT_GAP)) // 2

        # Draw HH:MM:SS
        x = self.draw_digit_pair(x, y, now.hour)
        
        # Colon 1
        self.draw_dots(x, y, [[0],[0],[1],[0],[1],[0],[0]]) # Simple vertical dots for colon
        x += COLON_W + SECTION_SPACING
        
        x = self.draw_digit_pair(x, y, now.minute)
        
        # Colon 2
        self.draw_dots(x, y, [[0],[0],[1],[0],[1],[0],[0]])
        x += COLON_W + SECTION_SPACING
        
        self.draw_digit_pair(x, y, now.second)

        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalClock(root)
    root.mainloop()
