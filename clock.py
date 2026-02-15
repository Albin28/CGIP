import tkinter as tk
import math
import datetime

# Constants for the clock
WIDTH = 400
HEIGHT = 400
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
RADIUS = 180

class AnalogClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Analog Clock Simulator (IST)")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        
        # Create the canvas for drawing
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()
        
        # Draw the static parts of the clock (Background, Dial)
        self.draw_clock_face()
        
        # Start the update loop
        self.update_clock()

    def draw_clock_face(self):
        """Draws the static clock face using Circle and Line primitives."""
        # Draw the main circle (Clock Dial)
        # Using create_oval to draw a circle
        self.canvas.create_oval(
            CENTER_X - RADIUS, CENTER_Y - RADIUS,
            CENTER_X + RADIUS, CENTER_Y + RADIUS,
            width=4, outline="black"
        )
        
        # Draw the center point
        self.canvas.create_oval(
            CENTER_X - 5, CENTER_Y - 5,
            CENTER_X + 5, CENTER_Y + 5,
            fill="black"
        )
        
        # Draw ticks for every minute (0 to 59)
        for i in range(60):
            angle = math.radians(i * 6)  # 360 degrees / 60 minutes = 6 degrees
            
            if i % 5 == 0:
                # Hour Tick (Thicker, Longer)
                x1 = CENTER_X + (RADIUS - 20) * math.sin(angle)
                y1 = CENTER_Y - (RADIUS - 20) * math.cos(angle)
                x2 = CENTER_X + RADIUS * math.sin(angle)
                y2 = CENTER_Y - RADIUS * math.cos(angle)
                self.canvas.create_line(x1, y1, x2, y2, width=3, fill="black")
                
                # Draw numbers only at hour marks
                text_x = CENTER_X + (RADIUS - 40) * math.sin(angle)
                text_y = CENTER_Y - (RADIUS - 40) * math.cos(angle)
                
                # Adjust number: 0 is 12
                # i // 5 gives 0, 1, 2... 11
                hour_num = i // 5
                num = hour_num if hour_num != 0 else 12
                self.canvas.create_text(text_x, text_y, text=str(num), font=("Arial", 14, "bold"))
            else:
                # Minute Tick (Thinner, Shorter)
                # "3 equidistant marks" concept: Standard clock has 4 marks between hours.
                x1 = CENTER_X + (RADIUS - 10) * math.sin(angle)
                y1 = CENTER_Y - (RADIUS - 10) * math.cos(angle)
                x2 = CENTER_X + RADIUS * math.sin(angle)
                y2 = CENTER_Y - RADIUS * math.cos(angle)
                self.canvas.create_line(x1, y1, x2, y2, width=1, fill="black")

    def get_ist_time(self):
        """Returns the current time in IST (UTC+5:30)."""
        # UTC time
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        # IST offset is +5:30
        ist_offset = datetime.timedelta(hours=5, minutes=30)
        ist_time = now_utc + ist_offset
        return ist_time

    def draw_hand(self, angle, length, width, color, kind="line"):
        """
        Draws a clock hand.
        angle: Angle in degrees (0 is 12 o'clock)
        length: Length of the hand
        width: Width of the line (if kind='line')
        color: Color of the hand
        kind: 'line' or 'polygon' to demonstrate different filling algorithms
        """
        # Convert angle to radians
        # -90 because standard math starts at 3 o'clock (0 rads), but clock starts at 12
        # Actually easier: use sin/cos with 12 o'clock logic directly
        # x = cx + r * sin(a), y = cy - r * cos(a) for 12 o'clock start
        
        rad_angle = math.radians(angle)
        
        if kind == "line":
            x_end = CENTER_X + length * math.sin(rad_angle)
            y_end = CENTER_Y - length * math.cos(rad_angle)
            
            # IDs are tagged so we can delete only hands later
            self.canvas.create_line(CENTER_X, CENTER_Y, x_end, y_end, width=width, fill=color, tags="hands")
            
        elif kind == "polygon":
            # For the hour hand, let's make a fancy pointer using a polygon
            # Tip of the hand
            x_tip = CENTER_X + length * math.sin(rad_angle)
            y_tip = CENTER_Y - length * math.cos(rad_angle)
            
            # Base width for the polygon triangle/rhombus
            base_w = width * 3 
            
            # Calculate base points perpendicular to the hand visual direction
            # Angle + 90 and Angle - 90
            rad_base_right = rad_angle + math.pi / 2
            rad_base_left = rad_angle - math.pi / 2
            
            x_base_r = CENTER_X + 10 * math.sin(rad_base_right)
            y_base_r = CENTER_Y - 10 * math.cos(rad_base_right)
            
            x_base_l = CENTER_X + 10 * math.sin(rad_base_left)
            y_base_l = CENTER_Y - 10 * math.cos(rad_base_left)
            
            # Draw polygon (Triangle/Arrow shape)
            # This demonstrates polygon filling
            self.canvas.create_polygon(x_tip, y_tip, x_base_r, y_base_r, CENTER_X, CENTER_Y, x_base_l, y_base_l, fill=color, tags="hands")

    def update_clock(self):
        """Updates the clock hands."""
        # 1. Fetch Time
        current_time = self.get_ist_time()
        
        # 2. Clear old hands
        self.canvas.delete("hands")
        
        # 3. Calculate Angles
        # Second Hand: 60 seconds = 360 degrees -> 6 deg per second
        seconds = current_time.second
        second_angle = seconds * 6
        
        # Minute Hand: 60 minutes = 360 degrees -> 6 deg per minute
        # Add seconds contribution for smooth movement (optional, but standard usually snaps or flows)
        # Let's keep it simple: snaps per minute + second contribution
        minutes = current_time.minute
        minute_angle = (minutes * 6) + (seconds * 0.1)
        
        # Hour Hand: 12 hours = 360 degrees -> 30 deg per hour
        hours = current_time.hour % 12
        hour_angle = (hours * 30) + (minutes * 0.5)
        
        # 4. Draw Hands using Primitives
        # Hour Hand (Polygon Filling)
        self.draw_hand(hour_angle, RADIUS * 0.5, 4, "black", kind="polygon")
        
        # Minute Hand (Line)
        self.draw_hand(minute_angle, RADIUS * 0.8, 6, "black", kind="line")
        
        # Second Hand (Line - Thin Red)
        self.draw_hand(second_angle, RADIUS * 0.9, 2, "red", kind="line")
        
        # Draw center cap again to cover hand bases
        self.canvas.create_oval(
            CENTER_X - 6, CENTER_Y - 6,
            CENTER_X + 6, CENTER_Y + 6,
            fill="red", outline="red", tags="hands"
        )
        
        # Update every 1000ms (1 second)
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalogClock(root)
    root.mainloop()
