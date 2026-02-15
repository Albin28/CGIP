import tkinter as tk
from tkinter import simpledialog, messagebox
import time

# Constants
WIDTH = 1000  # Wider to accommodate longer names
HEIGHT = 500
BG_COLOR = "black"
MAIN_COLOR = "#E0FFFF"   # Light Cyan
GLOW_COLOR = "#00FFFF"   # Cyan (Classic Neon)
HALO_COLOR = "#008B8B"   # Dark Cyan (faint glow)
STROKE_WIDTH = 3
HALO_WIDTH = 10
SPEED = 12  # Pixels per frame

# Character Grid
CHAR_W = 50
CHAR_H = 100
SPACING = 20

def get_char_strokes(char, x, y):
    """Returns a list of strokes (lists of points) for a given character at (x,y)."""
    c = char.upper()
    strokes = []
    
    # Helper to offset points
    def p(rel_x, rel_y):
        return (x + rel_x, y + rel_y)

    # Simplified Vector Font (A-Z, 0-9)
    if c == 'A':
        strokes = [[p(0, 100), p(25, 0), p(50, 100)], [p(10, 60), p(40, 60)]]
    elif c == 'B':
        strokes = [[p(0, 100), p(0, 0), p(40, 0), p(40, 50), p(0, 50)], [p(0, 50), p(50, 50), p(50, 100), p(0, 100)]]
    elif c == 'C':
        strokes = [[p(50, 25), p(50, 0), p(0, 0), p(0, 100), p(50, 100), p(50, 75)]]
    elif c == 'D':
        strokes = [[p(0, 100), p(0, 0), p(40, 0), p(50, 25), p(50, 75), p(40, 100), p(0, 100)]]
    elif c == 'E':
        strokes = [[p(50, 0), p(0, 0), p(0, 100), p(50, 100)], [p(0, 50), p(40, 50)]]
    elif c == 'F':
        strokes = [[p(50, 0), p(0, 0), p(0, 100)], [p(0, 50), p(40, 50)]]
    elif c == 'G':
        strokes = [[p(50, 25), p(50, 0), p(0, 0), p(0, 100), p(50, 100), p(50, 60), p(30, 60)]]
    elif c == 'H':
        strokes = [[p(0, 0), p(0, 100)], [p(50, 0), p(50, 100)], [p(0, 50), p(50, 50)]]
    elif c == 'I':
        strokes = [[p(0, 0), p(50, 0)], [p(25, 0), p(25, 100)], [p(0, 100), p(50, 100)]]
    elif c == 'J':
        strokes = [[p(0, 75), p(0, 100), p(25, 100), p(25, 0)]]
    elif c == 'K':
        strokes = [[p(0, 0), p(0, 100)], [p(50, 0), p(0, 50), p(50, 100)]]
    elif c == 'L':
        strokes = [[p(0, 0), p(0, 100), p(50, 100)]]
    elif c == 'M':
        strokes = [[p(0, 100), p(0, 0), p(25, 50), p(50, 0), p(50, 100)]]
    elif c == 'N':
        strokes = [[p(0, 100), p(0, 0), p(50, 100), p(50, 0)]]
    elif c == 'O':
        strokes = [[p(0, 0), p(50, 0), p(50, 100), p(0, 100), p(0, 0)]]
    elif c == 'P':
        strokes = [[p(0, 100), p(0, 0), p(50, 0), p(50, 50), p(0, 50)]]
    elif c == 'Q':
        strokes = [[p(0, 0), p(50, 0), p(50, 100), p(0, 100), p(0, 0)], [p(30, 80), p(50, 100)]]
    elif c == 'R':
        strokes = [[p(0, 100), p(0, 0), p(50, 0), p(50, 50), p(0, 50), p(50, 100)]]
    elif c == 'S':
        strokes = [[p(50, 0), p(0, 0), p(0, 50), p(50, 50), p(50, 100), p(0, 100)]]
    elif c == 'T':
        strokes = [[p(0, 0), p(50, 0)], [p(25, 0), p(25, 100)]]
    elif c == 'U':
        strokes = [[p(0, 0), p(0, 100), p(50, 100), p(50, 0)]]
    elif c == 'V':
        strokes = [[p(0, 0), p(25, 100), p(50, 0)]]
    elif c == 'W':
        strokes = [[p(0, 0), p(15, 100), p(25, 50), p(35, 100), p(50, 0)]]
    elif c == 'X':
        strokes = [[p(0, 0), p(50, 100)], [p(50, 0), p(0, 100)]]
    elif c == 'Y':
        strokes = [[p(0, 0), p(25, 50)], [p(50, 0), p(25, 50), p(25, 100)]]
    elif c == 'Z':
        strokes = [[p(0, 0), p(50, 0), p(0, 100), p(50, 100)]]
    elif c == ' ':
        strokes = [] # Space
    elif c == '-':
        strokes = [[p(0, 50), p(50, 50)]]
    else:
        # Default box for unknown
        strokes = [[p(0, 0), p(50, 0), p(50, 100), p(0, 100), p(0, 0)]]

    return strokes

class DigitalNameWriter:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Name Laser Plotter")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.canvas.pack()
        
        # Laser Cursor
        self.laser_cursor = self.canvas.create_oval(0, 0, 0, 0, fill="white", outline="white", tags="cursor")
        
        # Get User Input
        self.get_user_input()

    def get_user_input(self):
        text = simpledialog.askstring("Input", "Enter text to write (A-Z):", parent=self.root)
        if not text:
            text = "CGIP"
        
        self.prepare_strokes(text)
        self.root.after(500, self.process_next_operation)

    def prepare_strokes(self, text):
        self.operations = []
        
        # Calculate centering
        total_width = len(text) * (CHAR_W + SPACING) - SPACING
        start_x = (WIDTH - total_width) // 2
        start_y = (HEIGHT - CHAR_H) // 2
        
        current_x = start_x
        
        for char in text:
            strokes = get_char_strokes(char, current_x, start_y)
            for stroke in strokes:
                if not stroke: continue
                # Move to start of stroke
                self.operations.append(('jump', stroke[0]))
                # Draw to rest of points
                for point in stroke[1:]:
                    self.operations.append(('draw', point))
            
            current_x += CHAR_W + SPACING

        self.current_op_index = 0
        self.current_pos = None 
        self.drawing = False

    def process_next_operation(self):
        if self.current_op_index >= len(self.operations):
            self.finish_animation()
            return
            
        op_type, target = self.operations[self.current_op_index]
        
        if self.current_pos is None:
            # Initial placement
            self.current_pos = target
            self.move_cursor(target)
            self.current_op_index += 1
            self.process_next_operation()
            return

        self.drawing = (op_type == 'draw')
        self.target_pos = target
        
        self.animate_move()

    def animate_move(self):
        # Calculate vector
        dx = self.target_pos[0] - self.current_pos[0]
        dy = self.target_pos[1] - self.current_pos[1]
        dist = (dx**2 + dy**2)**0.5
        
        if dist <= SPEED:
            # Snap to target
            self.draw_segment(self.current_pos, self.target_pos)
            self.current_pos = self.target_pos
            self.move_cursor(self.target_pos)
            
            # Done with this op
            self.current_op_index += 1
            self.process_next_operation()
        else:
            # Move
            move_x = (dx / dist) * SPEED
            move_y = (dy / dist) * SPEED
            new_pos = (self.current_pos[0] + move_x, self.current_pos[1] + move_y)
            
            self.draw_segment(self.current_pos, new_pos)
            self.current_pos = new_pos
            self.move_cursor(new_pos)
            
            self.root.after(16, self.animate_move) 

    def draw_segment(self, p1, p2):
        if self.drawing:
            # Draw Halo (Glow)
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], 
                                    width=HALO_WIDTH, fill=HALO_COLOR, capstyle=tk.ROUND, tags="text_halo")
            # Draw Core
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], 
                                    width=STROKE_WIDTH, fill=MAIN_COLOR, capstyle=tk.ROUND, tags="text_core")

    def move_cursor(self, pos):
        r = 4
        self.canvas.coords(self.laser_cursor, pos[0]-r, pos[1]-r, pos[0]+r, pos[1]+r)
        self.canvas.tag_raise(self.laser_cursor)

    def finish_animation(self):
        self.canvas.delete(self.laser_cursor)
        self.canvas.create_text(WIDTH//2, HEIGHT - 50, text="SCAN COMPLETE", fill="#32CD32", font=("Courier", 16))
        
        # Retry Button
        btn = tk.Button(self.root, text="NEW TEXT", command=self.reset, font=("Arial", 12))
        btn.place(x=WIDTH//2 - 50, y=HEIGHT - 100)
        
    def reset(self):
        self.canvas.delete("all")
        self.laser_cursor = self.canvas.create_oval(0, 0, 0, 0, fill="white", outline="white", tags="cursor")
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        self.get_user_input()

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalNameWriter(root)
    root.mainloop()
