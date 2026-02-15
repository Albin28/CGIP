import tkinter as tk
from datetime import datetime, timedelta
import math

try:
    from global_land_mask import globe
    HAS_LAND_MASK = True
except ImportError:
    HAS_LAND_MASK = False
    print("Warning: global-land-mask not installed. Install with: pip install global-land-mask")
    print("Falling back to simple land approximation.")

class DaylightMap:
    def __init__(self, root):
        self.root = root
        self.root.title("Daylight Map Simulator")
        self.root.configure(bg='#1a1a2e')
        
        # Canvas dimensions
        self.width = 1200
        self.height = 600
        
        # Create canvas
        self.canvas = tk.Canvas(
            root, 
            width=self.width, 
            height=self.height,
            bg='#0f0f1e',
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)
        
        # Info label
        self.info_label = tk.Label(
            root,
            text="",
            font=('Consolas', 12),
            bg='#1a1a2e',
            fg='#ffffff'
        )
        self.info_label.pack(pady=10)
        
        # Dot grid settings (reduced by 1/3 for performance)
        self.dot_size = 1
        self.dot_spacing = 3
        
        # Map center - India (77°E) showing half the world
        self.center_longitude = 77.0  # India longitude
        self.longitude_range = 180.0   # Half the world
        
        # Time settings - 1 second in GUI = 864 seconds (14.4 minutes) in real world
        self.time_ratio = 864
        self.current_time = datetime.utcnow()
        
        # Colors for land and water
        self.land_day_color = '#90ee90'      # Light green for land (day)
        self.land_night_color = '#1a3a1a'    # Dark green for land (night)
        self.water_day_color = '#87ceeb'     # Light blue for water (day)
        self.water_night_color = '#0a1a2a'   # Dark blue for water (night)
        
        # Create the initial map
        self.draw_map()
        
        # Start animation
        self.animate()
    
    def calculate_solar_position(self, time):
        """
        Calculate the subsolar point (latitude and longitude where the sun is directly overhead)
        """
        # Days since J2000.0 (January 1, 2000, 12:00 UTC)
        j2000 = datetime(2000, 1, 1, 12, 0, 0)
        days_since_j2000 = (time - j2000).total_seconds() / 86400.0
        
        # Mean longitude of the Sun
        L = (280.460 + 0.9856474 * days_since_j2000) % 360
        
        # Mean anomaly
        g = (357.528 + 0.9856003 * days_since_j2000) % 360
        g_rad = math.radians(g)
        
        # Ecliptic longitude
        lambda_sun = L + 1.915 * math.sin(g_rad) + 0.020 * math.sin(2 * g_rad)
        lambda_rad = math.radians(lambda_sun)
        
        # Ecliptic obliquity
        epsilon = 23.439 - 0.0000004 * days_since_j2000
        epsilon_rad = math.radians(epsilon)
        
        # Solar declination (latitude where sun is overhead)
        declination = math.degrees(math.asin(math.sin(epsilon_rad) * math.sin(lambda_rad)))
        
        # Solar hour angle gives us longitude
        # Hours since midnight UTC
        hours_since_midnight = time.hour + time.minute / 60.0 + time.second / 3600.0
        
        # Equation of time (approximation)
        eqtime = -7.655 * math.sin(g_rad) + 9.873 * math.sin(2 * g_rad + math.radians(3.588))
        
        # Solar longitude (where the sun is directly overhead)
        solar_longitude = -15 * (hours_since_midnight - 12) - eqtime / 4
        
        return declination, solar_longitude
    
    def is_land(self, lat, lon):
        """
        Determine if a point at (lat, lon) is on land
        """
        if HAS_LAND_MASK:
            return globe.is_land(lat, lon)
        else:
            # Simple fallback: very rough approximation
            # This is just a simplified model - not accurate
            # Assumes land exists in certain latitude/longitude ranges
            # Major landmasses rough approximation
            if -30 <= lon <= 60 and 30 <= lat <= 70:  # Europe/Asia
                return True
            elif -130 <= lon <= -50 and 15 <= lat <= 70:  # North America
                return True
            elif -80 <= lon <= -35 and -55 <= lat <= 15:  # South America
                return True
            elif 10 <= lon <= 50 and -35 <= lat <= 35:  # Africa
                return True
            elif 110 <= lon <= 155 and -45 <= lat <= -10:  # Australia
                return True
            return False
    
    def is_daylight(self, lat, lon, solar_lat, solar_lon):
        """
        Determine if a point at (lat, lon) is in daylight
        Based on the angle between the point and the subsolar point
        """
        # Convert to radians
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        solar_lat_rad = math.radians(solar_lat)
        solar_lon_rad = math.radians(solar_lon)
        
        # Calculate angular distance using haversine formula
        dlon = lon_rad - solar_lon_rad
        dlat = lat_rad - solar_lat_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat_rad) * math.cos(solar_lat_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # If angular distance is less than 90 degrees (pi/2), it's daylight
        return c < math.pi / 2
    
    def draw_map(self):
        """
        Draw the pixelated map with dots
        """
        self.canvas.delete("all")
        
        # Calculate solar position
        solar_lat, solar_lon = self.calculate_solar_position(self.current_time)
        
        # Draw dots for each point on the globe
        for x in range(0, self.width, self.dot_spacing):
            for y in range(0, self.height, self.dot_spacing):
                # Convert pixel coordinates to lat/lon
                # Map shows India-centered hemisphere (180° longitude)
                lon = self.center_longitude - (self.longitude_range / 2) + (x / self.width) * self.longitude_range
                lat = 90 - (y / self.height) * 180
                
                # Determine if this point is on land
                is_land = self.is_land(lat, lon)
                
                # Determine if this point is in daylight
                is_day = self.is_daylight(lat, lon, solar_lat, solar_lon)
                
                # Select color based on land/water and day/night
                if is_land:
                    color = self.land_day_color if is_day else self.land_night_color
                else:
                    color = self.water_day_color if is_day else self.water_night_color
                
                # Draw the dot
                self.canvas.create_oval(
                    x - self.dot_size/2,
                    y - self.dot_size/2,
                    x + self.dot_size/2,
                    y + self.dot_size/2,
                    fill=color,
                    outline=color
                )
        
        # Update info label
        time_str = self.current_time.strftime("%Y-%m-%d %H:%M:%S UTC")
        self.info_label.config(
            text=f"Time: {time_str} | Solar Position: {solar_lat:.2f}°N, {solar_lon:.2f}°E | Speed: 1s = 14.4 min"
        )
    
    def animate(self):
        """
        Update the map every second with accelerated time
        """
        # Advance time by time_ratio seconds
        self.current_time += timedelta(seconds=self.time_ratio)
        
        # Redraw the map
        self.draw_map()
        
        # Schedule next update (1000ms = 1 second)
        self.root.after(1000, self.animate)

def main():
    root = tk.Tk()
    app = DaylightMap(root)
    root.mainloop()

if __name__ == "__main__":
    main()
