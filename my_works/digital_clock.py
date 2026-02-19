import tkinter as tk
import datetime

# Constants for the clock
WIDTH = 800
HEIGHT = 800
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

# Dot Matrix Settings (5x7)
DOT_SIZE = 8
DOT_GAP = 2
MATRIX_W, MATRIX_H = 5, 7
DIGIT_W = MATRIX_W * (DOT_SIZE + DOT_GAP) - DOT_GAP
DIGIT_SPACING = 10
SECTION_SPACING = 30 # Space between groups (HH MM SS)
COLON_W = DOT_SIZE

# Concentric Circle Settings
RADIUS_HOUR = 300
RADIUS_MINUTE = 280
RADIUS_SECOND = 260
CIRCLE_WIDTH = 10

# Digit Patterns (1=ON, 0=OFF) - 5x7 Matrix
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
        self.root.title("Digital Clock Simulator (IST) - Dot Matrix")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg="black")
        
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
        self.canvas.pack()
        
        self.update_clock()

    def get_ist_time(self):
        """Returns the current time in IST (UTC+5:30)."""
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        ist_offset = datetime.timedelta(hours=5, minutes=30)
        return now_utc + ist_offset

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
        
    def draw_colon(self, x, y):
        """Draws a colon using dots."""
        # Simple vertical dots for colon
        self.draw_dots(x, y, [[0],[0],[1],[0],[1],[0],[0]])
        return x + COLON_W + SECTION_SPACING

    def draw_circle_segments(self, radius, count, active_count, color_on, color_off, width=20):
        """Draws a segmented circle."""
        angle_per_segment = 360 / count
        gap_angle = 1 # gap between segments in degrees
        
        for i in range(count):
            start_angle = 90 - (i + 1) * angle_per_segment + gap_angle/2
            extent = angle_per_segment - gap_angle
            
            fill_color = color_on if i < active_count else color_off
            
            x0 = CENTER_X - radius
            y0 = CENTER_Y - radius
            x1 = CENTER_X + radius
            y1 = CENTER_Y + radius
            
            self.canvas.create_arc(x0, y0, x1, y1, start=start_angle, extent=extent, width=width, style=tk.ARC, outline=fill_color)

    def update_clock(self):
        current_time = self.get_ist_time()
        self.canvas.delete("all")
        
        h = current_time.hour
        m = current_time.minute
        s = current_time.second
        
        # --- Draw Concentric Circles ---
        self.draw_circle_segments(RADIUS_HOUR, 24, h, "#00FF00", "#112211", width=CIRCLE_WIDTH) # Green
        self.draw_circle_segments(RADIUS_MINUTE, 60, m, "#0000FF", "#111122", width=CIRCLE_WIDTH) # Blue
        self.draw_circle_segments(RADIUS_SECOND, 60, s, "#FF0000", "#221111", width=CIRCLE_WIDTH) # Red
        
        # --- Draw Digital Time (Centered) ---
        # Calculate total width
        grp_w = 2 * DIGIT_W + DIGIT_SPACING
        total_w = 3 * grp_w + 2 * (SECTION_SPACING + COLON_W + SECTION_SPACING) - 2 * SECTION_SPACING # Adjusted logic from previous
        # Let's re-calculate logic simply:
        # Width = (HH width) + (Space) + (Colon) + (Space) + (MM width) + ...
        # HH width = DIGIT_W + DIGIT_SPACING + DIGIT_W
        # Space + Colon + Space = SECTION_SPACING + COLON_W + SECTION_SPACING
        
        one_pair_width = 2 * DIGIT_W + DIGIT_SPACING
        colon_section_width = SECTION_SPACING + COLON_W + SECTION_SPACING
        
        total_clock_width = 3 * one_pair_width + 2 * colon_section_width
        
        x = CENTER_X - total_clock_width // 2
        y = CENTER_Y - (MATRIX_H * (DOT_SIZE + DOT_GAP)) // 2

        # Draw HH:MM:SS
        x = self.draw_digit_pair(x, y, h)
        
        # Colon 1
        self.draw_dots(x, y, [[0],[0],[1],[0],[1],[0],[0]]) 
        x += COLON_W + SECTION_SPACING
        
        x = self.draw_digit_pair(x, y, m)
        
        # Colon 2
        self.draw_dots(x, y, [[0],[0],[1],[0],[1],[0],[0]])
        x += COLON_W + SECTION_SPACING
        
        self.draw_digit_pair(x, y, s)

        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalClock(root)
    root.mainloop()