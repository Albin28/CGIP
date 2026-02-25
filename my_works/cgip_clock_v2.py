import tkinter as tk
import datetime
import math

# Constants
WIDTH, HEIGHT = 700, 700
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
BG_COLOR = "white"

class CGIPClockV2:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced CGIP Clock - Manual Algorithms")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()
        self.update_clock()

    # --- CGIP ALGORITHMS ---

    def draw_pixel(self, x, y, color):
        """Fundamental Step: Drawing a 'pixel' (represented as a small dot)."""
        size = 2
        self.canvas.create_rectangle(x, y, x + size, y + size, fill=color, outline="")

    def bresenham_line(self, x0, y0, x1, y1, color):
        """CGIP Algorithm: Bresenham's Line Drawing Algorithm."""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            self.draw_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def midpoint_circle(self, xc, yc, r, color):
        """CGIP Algorithm: Midpoint Circle Algorithm."""
        x = 0
        y = r
        p = 1 - r
        while x <= y:
            # Draw points in all 8 octants
            for px, py in [(xc+x, yc+y), (xc-x, yc+y), (xc+x, yc-y), (xc-x, yc-y),
                           (xc+y, yc+x), (xc-y, yc+x), (xc+y, yc-x), (xc-y, yc-x)]:
                self.draw_pixel(px, py, color)
            x += 1
            if p < 0:
                p += 2 * x + 1
            else:
                y -= 1
                p += 2 * (x - y) + 1

    # --- 2D TRANSFORMATIONS ---

    def rotate_point(self, x, y, angle_rad, cx, cy):
        """CGIP Transformation: Rotation around a pivot point (cx, cy)."""
        # Translation to origin
        tx, ty = x - cx, y - cy
        # Rotation
        rx = tx * math.cos(angle_rad) - ty * math.sin(angle_rad)
        ry = tx * math.sin(angle_rad) + ty * math.cos(angle_rad)
        # Translation back
        return rx + cx, ry + cy

    def scale_point(self, x, y, sx, sy, cx, cy):
        """CGIP Transformation: Scaling relative to a pivot point (cx, cy)."""
        tx, ty = x - cx, y - cy
        return (tx * sx) + cx, (ty * sy) + cy

    # --- CLOCK LOGIC ---

    def update_clock(self):
        self.canvas.delete("all")
        now = datetime.datetime.now()
        h, m, s = now.hour % 12, now.minute, now.second

        # 1. Draw Static Rings (Midpoint Circle)
        for r in [280, 260, 240]:
            self.midpoint_circle(CENTER_X, CENTER_Y, r, "#EEEEEE")

        # 2. Draw Hour Markers (Rotation Transformation)
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            x0, y0 = CENTER_X + 260, CENTER_Y
            x1, y1 = CENTER_X + 280, CENTER_Y
            px0, py0 = self.rotate_point(x0, y0, angle, CENTER_X, CENTER_Y)
            px1, py1 = self.rotate_point(x1, y1, angle, CENTER_X, CENTER_Y)
            self.bresenham_line(int(px0), int(py0), int(px1), int(py1), "#3F51B5")

        # 3. Draw Hands (Bresenham + Rotation)
        hands = [(h * 30 + m/2, 160, "#3F51B5", 4), (m * 6, 220, "#009688", 3), (s * 6, 250, "#FF5722", 1)]
        for angle_deg, length, color, thickness in hands:
            angle = math.radians(angle_deg - 90)
            ex, ey = CENTER_X + length, CENTER_Y
            px, py = self.rotate_point(ex, ey, angle, CENTER_X, CENTER_Y)
            # Simulating thickness with multiple lines if needed, but keeping it simple for viva
            for offset in range(thickness):
                self.bresenham_line(CENTER_X, CENTER_Y + offset, int(px), int(py) + offset, color)

        # 4. Animated Center Pulse (Scaling Transformation)
        # Using microsecond for a smooth pulse effect
        ms = datetime.datetime.now().microsecond
        s_pulse = 1.0 + 0.15 * math.sin(ms / 100000)
        self.midpoint_circle(CENTER_X, CENTER_Y, int(6 * s_pulse), "#212121")

        # CGIP Notes for Viva:
        # - Bresenham's: Choice of integer-only math for efficiency.
        # - Midpoint: Uses symmetry (8 octants) to reduce computation.
        # - Rotation: Uses sin/cos to translate angular time to (x,y) coordinates.
        # - Scaling: Dynamically changes radius/size based on a pulse factor.

        self.root.after(50, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = CGIPClockV2(root)
    time_counter = 0 # Not strictly needed but for logic
    root.mainloop()
