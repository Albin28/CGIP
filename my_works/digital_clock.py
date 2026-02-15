import tkinter as tk
import datetime
import math

# Constants for the clock
WIDTH = 800
HEIGHT = 800
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

# Digital Clock Segment Settings (Larger)
SEGMENT_LENGTH = 25
SEGMENT_WIDTH = 5
GAP = 15  # Gap between digits (Increased)

# Concentric Circle Settings
# Radius for each circle
RADIUS_HOUR = 300
RADIUS_MINUTE = 280
RADIUS_SECOND = 260
CIRCLE_WIDTH = 10

# 7-Segment Definitions (Same as before)
#   A
# F   B
#   G
# E   C
#   D
# Segments: A, B, C, D, E, F, G
# 0: A, B, C, D, E, F
# 1: B, C
# 2: A, B, D, E, G
# 3: A, B, C, D, G
# 4: B, C, F, G
# 5: A, C, D, F, G
# 6: A, C, D, E, F, G
# 7: A, B, C
# 8: A, B, C, D, E, F, G
# 9: A, B, C, D, F, G

class DigitalClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock Simulator (IST) - Concentric Circles")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg="black")
        
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
        self.canvas.pack()
        
        # Start the update loop
        self.update_clock()

    def get_ist_time(self):
        """Returns the current time in IST (UTC+5:30)."""
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        ist_offset = datetime.timedelta(hours=5, minutes=30)
        return now_utc + ist_offset

    def draw_segment(self, x, y, vertical=False, on=True):
        """Draws a single segment using create_polygon."""
        color = "#00FF00" if on else "#112211"  # Bright Green for ON, Dim Green for OFF
        
        if vertical:
            # Vertical Segment (Width x Length)
            points = [
                x, y,
                x + SEGMENT_WIDTH, y + SEGMENT_WIDTH,
                x + SEGMENT_WIDTH, y + SEGMENT_LENGTH - SEGMENT_WIDTH,
                x, y + SEGMENT_LENGTH,
                x - SEGMENT_WIDTH, y + SEGMENT_LENGTH - SEGMENT_WIDTH,
                x - SEGMENT_WIDTH, y + SEGMENT_WIDTH
            ]
        else:
            # Horizontal Segment (Length x Width)
            points = [
                x, y,
                x + SEGMENT_WIDTH, y - SEGMENT_WIDTH,
                x + SEGMENT_LENGTH - SEGMENT_WIDTH, y - SEGMENT_WIDTH,
                x + SEGMENT_LENGTH, y,
                x + SEGMENT_LENGTH - SEGMENT_WIDTH, y + SEGMENT_WIDTH,
                x + SEGMENT_WIDTH, y + SEGMENT_WIDTH
            ]
        
        self.canvas.create_polygon(*points, fill=color, outline="")

    def draw_digit(self, x, y, digit):
        """Draws a digit (0-9) at (x, y)."""
        # A: Top Horizontal
        self.draw_segment(x + SEGMENT_WIDTH, y, vertical=False, on=digit in [0, 2, 3, 5, 6, 7, 8, 9])
        
        # B: Top Right Vertical
        self.draw_segment(x + SEGMENT_LENGTH + SEGMENT_WIDTH, y + SEGMENT_WIDTH, vertical=True, on=digit in [0, 1, 2, 3, 4, 7, 8, 9])
        
        # C: Bottom Right Vertical
        self.draw_segment(x + SEGMENT_LENGTH + SEGMENT_WIDTH, y + SEGMENT_LENGTH + 2*SEGMENT_WIDTH, vertical=True, on=digit in [0, 1, 3, 4, 5, 6, 7, 8, 9])
        
        # D: Bottom Horizontal
        self.draw_segment(x + SEGMENT_WIDTH, y + 2*SEGMENT_LENGTH + 2*SEGMENT_WIDTH, vertical=False, on=digit in [0, 2, 3, 5, 6, 8, 9])
        
        # E: Bottom Left Vertical
        self.draw_segment(x - SEGMENT_WIDTH, y + SEGMENT_LENGTH + 2*SEGMENT_WIDTH, vertical=True, on=digit in [0, 2, 6, 8])
        
        # F: Top Left Vertical
        self.draw_segment(x - SEGMENT_WIDTH, y + SEGMENT_WIDTH, vertical=True, on=digit in [0, 4, 5, 6, 8, 9])
        
        # G: Middle Horizontal
        self.draw_segment(x + SEGMENT_WIDTH, y + SEGMENT_LENGTH + SEGMENT_WIDTH, vertical=False, on=digit in [2, 3, 4, 5, 6, 8, 9])

    def draw_colon(self, x, y):
        """Draws a colon."""
        self.canvas.create_oval(x, y + SEGMENT_LENGTH/2, x+4, y + SEGMENT_LENGTH/2 + 4, fill="#00FF00", outline="")
        self.canvas.create_oval(x, y + 1.5*SEGMENT_LENGTH, x+4, y + 1.5*SEGMENT_LENGTH + 4, fill="#00FF00", outline="")

    def draw_circle_segments(self, radius, count, active_count, color_on, color_off, width=20):
        """Draws a segmented circle."""
        angle_per_segment = 360 / count
        gap_angle = 1 # gap between segments in degrees
        
        # Start from top (90 degrees in standard math, but Tkinter 0 is East/Right)
        # Tkinter arc: start is angle from East (counter-clockwise).
        # We want top (90 deg) to be 0 for clock.
        # So index 0 (top) is 90 degrees. Index 1 is 90 - angle_per_segment, etc.
        
        for i in range(count):
            # Calculate start angle for this segment
            # i=0 -> start at 90.
            # i increments -> angle decreases (clockwise)
            start_angle = 90 - (i + 1) * angle_per_segment + gap_angle/2
            extent = angle_per_segment - gap_angle
            
            # Correction to handle tkinter's angle system if needed, but standard 0-360 works fine.
            # active_count is 1-based (1 to 60 or 0 to 59?). User said "increase by one unit".
            # If active_count = 10, then segments 0 to 9 are ON.
            
            fill_color = color_on if i < active_count else color_off
            
            # Bounding box for the arc
            x0 = CENTER_X - radius
            y0 = CENTER_Y - radius
            x1 = CENTER_X + radius
            y1 = CENTER_Y + radius
            
            self.canvas.create_arc(x0, y0, x1, y1, start=start_angle, extent=extent, width=width, style=tk.ARC, outline=fill_color)


    def update_clock(self):
        current_time = self.get_ist_time()
        
        # Clear canvas
        self.canvas.delete("all")
        
        h = current_time.hour
        m = current_time.minute
        s = current_time.second
        
        # --- Draw Concentric Circles ---
        
        # Hour Circle (Green) - Outer - 24 Segments
        # User said "Green circle which represent hour and only has 24 segment"
        # Since it's digital 24h format, we use 0-23.
        # At midnight (00), segments should be off (black).
        self.draw_circle_segments(RADIUS_HOUR, 24, h, "#00FF00", "#112211", width=CIRCLE_WIDTH) # Green
        
        # Minute Circle (Blue) - Middle - 60 Segments
        self.draw_circle_segments(RADIUS_MINUTE, 60, m, "#0000FF", "#111122", width=CIRCLE_WIDTH) # Blue
        
        # Second Circle (Red) - Inner - 60 Segments
        # "Innermost red circle represent sec and is divided into 60 part... after 60 sec it become a full red circle"
        self.draw_circle_segments(RADIUS_SECOND, 60, s, "#FF0000", "#221111", width=CIRCLE_WIDTH) # Red
        
        
        # --- Draw Digital Clock (Centered) ---
        
        # Calculate total width of the digital clock to center it
        # Digit width = SEGMENT_LENGTH + 2*SEGMENT_WIDTH + GAP
        # 6 Digits + 2 Colons + Spacing
        # Structure: [D][gap][D] [s] [:] [s] [D][gap][D] [s] [:] [s] [D][gap][D]
        # Let's approximate or calculate exactly.
        
        digit_w = SEGMENT_LENGTH + 2*SEGMENT_WIDTH # Width of one digit content
        digit_spacing = GAP
        section_spacing = 40 # Space between HH and MM (Increased)
        colon_width = 10
        
        # Total Width Calculation
        # HH
        w_h = 2 * digit_w + digit_spacing
        # MM
        w_m = 2 * digit_w + digit_spacing
        # SS
        w_s = 2 * digit_w + digit_spacing
        
        total_clock_width = w_h + section_spacing + colon_width + section_spacing + w_m + section_spacing + colon_width + section_spacing + w_s
        
        # Start X
        start_x = CENTER_X - total_clock_width // 2
        # Start Y (Centered vertically)
        start_y = CENTER_Y - (2*SEGMENT_LENGTH + 3*SEGMENT_WIDTH) // 2
        
        curr_x = start_x
        
        # Draw Hours
        self.draw_digit(curr_x, start_y, h // 10)
        curr_x += digit_w + digit_spacing
        self.draw_digit(curr_x, start_y, h % 10)
        curr_x += digit_w + section_spacing
        
        # Colon
        self.draw_colon(curr_x, start_y)
        curr_x += colon_width + section_spacing
        
        # Draw Minutes
        self.draw_digit(curr_x, start_y, m // 10)
        curr_x += digit_w + digit_spacing
        self.draw_digit(curr_x, start_y, m % 10)
        curr_x += digit_w + section_spacing
        
        # Colon
        self.draw_colon(curr_x, start_y)
        curr_x += colon_width + section_spacing
        
        # Draw Seconds
        self.draw_digit(curr_x, start_y, s // 10)
        curr_x += digit_w + digit_spacing
        self.draw_digit(curr_x, start_y, s % 10)

        # Update every 1000ms
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalClock(root)
    root.mainloop()
