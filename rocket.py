import tkinter as tk
import time
import random

# Constants
WIDTH = 400
HEIGHT = 600
ROCKET_WIDTH = 20  # Smaller width
ROCKET_HEIGHT = 40 # Smaller height
GROUND_HEIGHT = 50
LAUNCH_DURATION = 12.0 # Increased duration

# Colors
SKY_START = (135, 206, 235) # SkyBlue
SKY_END = (10, 10, 30)      # Deep Space Blue/Black
STARS_COLOR = "white"
MOON_COLOR = "#F4F6F0"      # Off-white

def interpolate_color(start_rgb, end_rgb, t):
    """Interpolates between two RGB tuples based on t (0.0 to 1.0)."""
    t = max(0.0, min(1.0, t))
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
    return f"#{r:02x}{g:02x}{b:02x}"

class RocketSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Rocket Launch Simulation")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg=interpolate_color(SKY_START, SKY_END, 0))
        self.canvas.pack()
        
        # Generate random stars (x, y, size)
        self.stars = []
        for _ in range(50):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT - GROUND_HEIGHT)
            size = random.randint(1, 3)
            self.stars.append((x, y, size))
            
        self.launch_button = tk.Button(self.root, text="LAUNCH", command=self.launch, 
                                       font=("Helvetica", 12, "bold"), bg="#ff4500", fg="white", 
                                       activebackground="#ff6347", activeforeground="white", relief="flat", padx=15, pady=8)
        self.launch_button.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")
        
        self.retry_button = None
        
        self.rocket_y = HEIGHT - GROUND_HEIGHT - ROCKET_HEIGHT
        self.start_y = self.rocket_y
        self.is_launching = False
        self.start_time = 0
        
        self.draw_scenery(0)
        self.draw_rocket(WIDTH // 2, self.rocket_y)

    def draw_scenery(self, t):
        self.canvas.delete("scenery")
        
        # 1. Sky Color
        sky_color = interpolate_color(SKY_START, SKY_END, t)
        self.canvas.config(bg=sky_color)
        
        # 2. Stars (Fade in as t increases)
        if t > 0.2:
            # Simple fade in simulation: change color from sky to white
            # Since we can't easily do alpha on individual items in basic tkinter canvas without complex hex math per star,
            # we'll just draw them if t is high enough, or we can interpolate their color too.
            # Let's interpolate their color from Sky Color to White.
            
            # Current Sky RGB
            curr_sky_r = int(SKY_START[0] + (SKY_END[0] - SKY_START[0]) * t)
            curr_sky_g = int(SKY_START[1] + (SKY_END[1] - SKY_START[1]) * t)
            curr_sky_b = int(SKY_START[2] + (SKY_END[2] - SKY_START[2]) * t)
            sky_rgb = (curr_sky_r, curr_sky_g, curr_sky_b)
            
            star_color = interpolate_color(sky_rgb, (255, 255, 255), (t - 0.2) * 1.5) # accelerate star fade in
            
            for x, y, size in self.stars:
                self.canvas.create_oval(x, y, x + size, y + size, fill=star_color, outline=star_color, tags="scenery")

        # 3. Moon (Full moon top right)
        # Verify visibility based on t? Or always there? 
        # Requirement: "as it rises the sky colour gradually changes... and a full moon of right corner"
        # It implies the moon becomes visible or is part of the night sky.
        # Let's fade it in similar to stars, or just have it there but faint.
        # Let's make it fully visible when t is high.
        if t > 0.1:
            moon_alpha = min(1.0, (t - 0.1) * 2)
            # Interpolate moon color from sky to Moon Color
            # This is a bit hacky visually but effective for "fading in" on solid backgrounds
            mk_sky_r = int(SKY_START[0] + (SKY_END[0] - SKY_START[0]) * t)
            mk_sky_g = int(SKY_START[1] + (SKY_END[1] - SKY_START[1]) * t)
            mk_sky_b = int(SKY_START[2] + (SKY_END[2] - SKY_START[2]) * t)
            sky_rgb = (mk_sky_r, mk_sky_g, mk_sky_b)
             
            # Moon distinct color
            moon_r, moon_g, moon_b = 244, 246, 240
            
            final_moon_color = interpolate_color(sky_rgb, (moon_r, moon_g, moon_b), moon_alpha)
            
            mx, my = WIDTH - 50, 50
            r = 30
            self.canvas.create_oval(mx - r, my - r, mx + r, my + r, fill=final_moon_color, outline=final_moon_color, tags="scenery")
            
            # Craters (simple details)
            if t > 0.5:
                 crater_color = interpolate_color(sky_rgb, (200, 200, 200), moon_alpha)
                 self.canvas.create_oval(mx - 10, my - 10, mx - 2, my - 2, fill=crater_color, outline=crater_color, tags="scenery")
                 self.canvas.create_oval(mx + 5, my + 8, mx + 15, my + 15, fill=crater_color, outline=crater_color, tags="scenery")

        # 4. Ground (Moves down or disappears?)
        # Let's keep it fixed at bottom but it goes out of view as we ascend?
        # Simulation says "rocket launches to certain height". 
        # Usually that means rocket moves UP.
        # To simulate high altitude, ground should move down off screen.
        ground_y = HEIGHT - GROUND_HEIGHT + (t * HEIGHT) # Move ground down as t increases
        if ground_y < HEIGHT:
            self.canvas.create_rectangle(0, ground_y, WIDTH, HEIGHT + (t*HEIGHT), fill="#228B22", outline="#228B22", tags="scenery")
        
    def draw_rocket(self, x, y):
        self.canvas.delete("rocket")
        
        # Modern Look: Sleek, Silver/White, aerodynamic
        
        # Fins (Dark Blue)
        self.canvas.create_polygon(x - ROCKET_WIDTH//2, y + ROCKET_HEIGHT - 5, 
                                   x - ROCKET_WIDTH, y + ROCKET_HEIGHT + 10, 
                                   x - ROCKET_WIDTH//2, y + ROCKET_HEIGHT - 15, 
                                   fill="#191970", outline="#191970", tags="rocket") # Left fin
                                   
        self.canvas.create_polygon(x + ROCKET_WIDTH//2, y + ROCKET_HEIGHT - 5, 
                                   x + ROCKET_WIDTH, y + ROCKET_HEIGHT + 10, 
                                   x + ROCKET_WIDTH//2, y + ROCKET_HEIGHT - 15, 
                                   fill="#191970", outline="#191970", tags="rocket") # Right fin

        # Body (Silver/Light Grey gradient simulated by two rects or just one sleek color)
        self.canvas.create_rectangle(x - ROCKET_WIDTH//2, y, x + ROCKET_WIDTH//2, y + ROCKET_HEIGHT, 
                                     fill="#E0E0E0", outline="#A0A0A0", tags="rocket")
        
        # Nose cone (Red or Dark Blue to match fins? Let's go Red for visibility)
        self.canvas.create_polygon(x - ROCKET_WIDTH//2, y, 
                                   x, y - 15, 
                                   x + ROCKET_WIDTH//2, y, 
                                   fill="#DC143C", outline="#DC143C", tags="rocket")
        
        # Window (Circular, cyan)
        self.canvas.create_oval(x - 5, y + 10, x + 5, y + 20, fill="#00FFFF", outline="#4682B4", width=1, tags="rocket")

        # Flame (Animated if launching)
        if self.is_launching:
             # Flicker effect
             flicker = random.randint(0, 5)
             self.canvas.create_polygon(x - 5, y + ROCKET_HEIGHT, 
                                        x, y + ROCKET_HEIGHT + 20 + flicker, 
                                        x + 5, y + ROCKET_HEIGHT, 
                                        fill="#FF4500", outline="#FF4500", tags="rocket")
             self.canvas.create_polygon(x - 3, y + ROCKET_HEIGHT, 
                                        x, y + ROCKET_HEIGHT + 12 + flicker, 
                                        x + 3, y + ROCKET_HEIGHT, 
                                        fill="#FFD700", outline="#FFD700", tags="rocket")

    def launch(self):
        if not self.is_launching:
            self.is_launching = True
            self.start_time = time.time()
            self.launch_button.place_forget()
            self.update_simulation()
            
    def update_simulation(self):
        if self.is_launching:
            elapsed_time = time.time() - self.start_time
            t = elapsed_time / LAUNCH_DURATION
            
            if t <= 1.0:
                # 1. Update Sky/Scenery
                self.draw_scenery(t)
                
                # 2. Move Rocket
                # Initial slow acceleration then constant speed?
                # Or just move up linear for simplicity.
                # It needs to stay somewhat on screen or just move up?
                # "clicking it lauches the rocket to certain height"
                # Let's move it to 1/3rd of screen and hold it there while background moves?
                # Or just move it up.
                
                # Let's move rocket UP.
                # Target Y is something like 100 (near top)
                # visible range: start_y -> 100
                progress = t 
                current_y = self.start_y - (self.start_y - 150) * progress
                self.rocket_y = current_y
                
                self.draw_rocket(WIDTH // 2, self.rocket_y)
                
                self.root.after(20, self.update_simulation)
            else:
                self.finish_simulation()
                
    def finish_simulation(self):
        self.is_launching = False
        self.canvas.delete("all")
        self.canvas.config(bg="black") 
        
        # Retry Screen
        self.canvas.create_text(WIDTH//2, HEIGHT//2 - 50, text="Mission Accomplished", fill="white", font=("Helvetica", 24, "bold"))
        
        self.retry_button = tk.Button(self.root, text="RETRY MISSION", command=self.reset, 
                                      font=("Helvetica", 14, "bold"), bg="#32CD32", fg="white", 
                                      relief="flat", padx=20, pady=10)
        self.retry_button.place(x=WIDTH//2 - 90, y=HEIGHT//2)

    def reset(self):
        if self.retry_button:
            self.retry_button.destroy()
            self.retry_button = None
            
        self.rocket_y = HEIGHT - GROUND_HEIGHT - ROCKET_HEIGHT
        self.start_y = self.rocket_y
        self.draw_scenery(0)
        self.draw_rocket(WIDTH // 2, self.rocket_y)
        self.launch_button.place(x=WIDTH//2 - 60, y=HEIGHT - 80)

if __name__ == "__main__":
    root = tk.Tk()
    app = RocketSimulation(root)
    root.mainloop()
