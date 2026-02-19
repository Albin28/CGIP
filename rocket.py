import tkinter as tk
import time
import random

WIDTH, HEIGHT = 400, 600
ROCKET_W, ROCKET_H = 20, 40
GROUND_H, LAUNCH_DUR = 50, 12.0
SKY_START = (135, 206, 235)
SKY_END = (10, 10, 30)

def interpolate_color(start_rgb, end_rgb, t):
    t = max(0.0, min(1.0, t))
    return "#{:02x}{:02x}{:02x}".format(*(int(s + (e - s) * t) for s, e in zip(start_rgb, end_rgb)))

class RocketSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Rocket Launch Simulation")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg=interpolate_color(SKY_START, SKY_END, 0))
        self.canvas.pack()
        
        self.stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT - GROUND_H), random.randint(1, 3)) 
                      for _ in range(50)]
            
        self.launch_btn = tk.Button(self.root, text="LAUNCH", command=self.launch, 
                                    font=("Helvetica", 12, "bold"), bg="#ff4500", fg="white")
        self.launch_btn.place(relx=0.5, rely=0.9, anchor="center")
        
        self.retry_btn = None
        self.reset_vars()

    def reset_vars(self):
        self.rocket_y = HEIGHT - GROUND_H - ROCKET_H
        self.start_y = self.rocket_y
        self.is_launching = False
        self.start_time = 0
        self.draw_scenery(0)
        self.draw_rocket(WIDTH // 2, self.rocket_y)

    def draw_scenery(self, t):
        self.canvas.delete("scenery")
        curr_sky = tuple(int(s + (e - s) * t) for s, e in zip(SKY_START, SKY_END))
        self.canvas.config(bg=interpolate_color(SKY_START, SKY_END, t))
        
        # Stars
        if t > 0.2:
            star_fill = interpolate_color(curr_sky, (255, 255, 255), (t - 0.2) * 1.5)
            for x, y, size in self.stars:
                self.canvas.create_oval(x, y, x + size, y + size, fill=star_fill, outline=star_fill, tags="scenery")

        # Moon
        if t > 0.1:
            alpha = min(1.0, (t - 0.1) * 2)
            moon_fill = interpolate_color(curr_sky, (244, 246, 240), alpha)
            mx, my, r = WIDTH - 50, 50, 30
            self.canvas.create_oval(mx - r, my - r, mx + r, my + r, fill=moon_fill, outline=moon_fill, tags="scenery")
            
            if t > 0.5: # Craters
                c_fill = interpolate_color(curr_sky, (200, 200, 200), alpha)
                self.canvas.create_oval(mx - 10, my - 10, mx - 2, my - 2, fill=c_fill, outline=c_fill, tags="scenery")

        # Ground
        ground_y = HEIGHT - GROUND_H + (t * HEIGHT)
        if ground_y < HEIGHT:
            self.canvas.create_rectangle(0, ground_y, WIDTH, HEIGHT * (1 + t), fill="#228B22", outline="#228B22", tags="scenery")

    def draw_rocket(self, x, y):
        self.canvas.delete("rocket")
        rw, rh = ROCKET_W, ROCKET_H
        
        # Fins
        fin_color = "#191970"
        self.canvas.create_polygon(x - rw//2, y + rh - 5, x - rw, y + rh + 10, x - rw//2, y + rh - 15, 
                                   fill=fin_color, outline=fin_color, tags="rocket")
        self.canvas.create_polygon(x + rw//2, y + rh - 5, x + rw, y + rh + 10, x + rw//2, y + rh - 15, 
                                   fill=fin_color, outline=fin_color, tags="rocket")

        # Body & Nose
        self.canvas.create_rectangle(x - rw//2, y, x + rw//2, y + rh, fill="#E0E0E0", outline="#A0A0A0", tags="rocket")
        self.canvas.create_polygon(x - rw//2, y, x, y - 15, x + rw//2, y, fill="#DC143C", outline="#DC143C", tags="rocket")
        
        # Window
        self.canvas.create_oval(x - 5, y + 10, x + 5, y + 20, fill="#00FFFF", outline="#4682B4", width=1, tags="rocket")

        # Flame
        if self.is_launching:
            flicker = random.randint(0, 5)
            self.canvas.create_polygon(x - 5, y + rh, x, y + rh + 20 + flicker, x + 5, y + rh, 
                                       fill="#FF4500", outline="#FF4500", tags="rocket")
            self.canvas.create_polygon(x - 3, y + rh, x, y + rh + 12 + flicker, x + 3, y + rh, 
                                       fill="#FFD700", outline="#FFD700", tags="rocket")

    def launch(self):
        if not self.is_launching:
            self.is_launching = True
            self.start_time = time.time()
            self.launch_btn.place_forget()
            self.update_simulation()
            
    def update_simulation(self):
        if not self.is_launching: return
        t = (time.time() - self.start_time) / LAUNCH_DURATION
        
        if t <= 1.0:
            self.draw_scenery(t)
            self.rocket_y = self.start_y - (self.start_y - 100) * t
            self.draw_rocket(WIDTH // 2, self.rocket_y)
            self.root.after(20, self.update_simulation)
        else:
            self.finish_simulation()
                
    def finish_simulation(self):
        self.is_launching = False
        self.canvas.delete("all")
        self.canvas.config(bg="black") 
        self.canvas.create_text(WIDTH//2, HEIGHT//2 - 50, text="Mission Accomplished", fill="white", font=("Helvetica", 24, "bold"))
        
        self.retry_btn = tk.Button(self.root, text="RETRY MISSION", command=self.reset, 
                                   font=("Helvetica", 14, "bold"), bg="#32CD32", fg="white")
        self.retry_btn.place(relx=0.5, rely=0.6, anchor="center")

    def reset(self):
        if self.retry_btn:
            self.retry_btn.destroy()
            self.retry_btn = None
        self.reset_vars()
        self.launch_btn.place(relx=0.5, rely=0.9, anchor="center")

if __name__ == "__main__":
    root = tk.Tk()
    app = RocketSimulation(root)
    root.mainloop()
