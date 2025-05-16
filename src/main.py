"""Main entry point for the orbital simulation."""

import sys
import pygame
import numpy as np
from physics.constants import EARTH_RADIUS, SCALE_FACTOR, TIME_STEP
from physics.orbital_mechanics import OrbitalBody

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Orbital Simulation")

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Simulation controls
MAX_TRAJECTORY_POINTS = 1000
TRAJECTORY_DISPLAY_FRACTION = 0.15  # Show last 15% of trajectory
BASE_VELOCITY_CHANGE = 50.0  # Base m/s per key press
ACCELERATION_FACTOR = 1.2  # How quickly the velocity change increases
MAX_VELOCITY_CHANGE = 2000.0  # Maximum m/s per frame
TIME_SCALE_CHANGE = 0.5  # Time scale change per key press
MIN_TIME_SCALE = 0.1
MAX_TIME_SCALE = 10.0

def screen_coords(position):
    """Convert simulation coordinates to screen coordinates."""
    return (
        int(WINDOW_WIDTH / 2 + position[0] * SCALE_FACTOR),
        int(WINDOW_HEIGHT / 2 - position[1] * SCALE_FACTOR)  # Flip y-axis
    )

def draw_earth():
    """Draw Earth at the center of the screen."""
    center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    radius = int(EARTH_RADIUS * SCALE_FACTOR)
    pygame.draw.circle(screen, BLUE, center, radius)

def draw_satellite(position):
    """Draw a diamond-shaped satellite at the given position."""
    x, y = screen_coords(position)
    size = 8  # Size of the diamond
    
    # Define diamond points (clockwise from top)
    points = [
        (x, y - size),  # Top
        (x + size, y),  # Right
        (x, y + size),  # Bottom
        (x - size, y)   # Left
    ]
    
    # Draw diamond
    pygame.draw.polygon(screen, RED, points)

def draw_trajectory(trajectory):
    """Draw the trajectory of the satellite with fade effect."""
    if len(trajectory) < 2:
        return
    
    # Calculate how many points to show (15% of total)
    display_points = max(2, int(len(trajectory) * TRAJECTORY_DISPLAY_FRACTION))
    visible_trajectory = trajectory[-display_points:]
    
    # Convert trajectory points to screen coordinates
    points = [screen_coords(pos) for pos in visible_trajectory]
    
    # Draw fading trajectory segments
    for i in range(len(points) - 1):
        # Calculate alpha value (0-255) based on position in trajectory
        alpha = int(255 * (i / (len(points) - 1)))
        color = (WHITE[0], WHITE[1], WHITE[2], alpha)
        
        # Create a surface for this line segment
        line_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(line_surface, color, points[i], points[i + 1], 1)
        screen.blit(line_surface, (0, 0))

def draw_info(time_scale, velocity, velocity_change):
    """Draw simulation information."""
    font = pygame.font.Font(None, 36)
    
    # Display time scale
    time_text = font.render(f"Time Scale: {time_scale:.1f}x", True, WHITE)
    screen.blit(time_text, (10, 10))
    
    # Display velocity
    vel_magnitude = np.linalg.norm(velocity)
    vel_text = font.render(f"Velocity: {vel_magnitude/1000:.1f} km/s", True, WHITE)
    screen.blit(vel_text, (10, 50))
    
    # Display velocity change rate
    rate_text = font.render(f"Acceleration: {velocity_change:.0f} m/s", True, WHITE)
    screen.blit(rate_text, (10, 90))
    
    # Display controls
    controls = [
        "Controls:",
        "Arrow Keys: Adjust velocity (hold to accelerate)",
        "+/-: Adjust time scale",
        "ESC: Quit"
    ]
    
    for i, text in enumerate(controls):
        control_text = font.render(text, True, GRAY)
        screen.blit(control_text, (10, 140 + i * 30))

def main():
    """Main game loop."""
    clock = pygame.time.Clock()
    
    # Initialize orbital body (starting from 10,000 km above Earth's surface)
    initial_position = np.array([0, EARTH_RADIUS + 10_000_000])  # 10,000 km above Earth
    initial_velocity = np.array([7800.0, 0.0])  # Approximate orbital velocity in m/s
    satellite = OrbitalBody(initial_position, initial_velocity)
    
    # Simulation control variables
    time_scale = 1.0
    velocity_change = BASE_VELOCITY_CHANGE
    last_key_state = pygame.key.get_pressed()
    
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    time_scale = min(MAX_TIME_SCALE, time_scale + TIME_SCALE_CHANGE)
                elif event.key == pygame.K_MINUS:
                    time_scale = max(MIN_TIME_SCALE, time_scale - TIME_SCALE_CHANGE)
        
        # Handle continuous key presses for velocity adjustment
        keys = pygame.key.get_pressed()
        
        # Check if any arrow key is being held
        arrow_keys_held = any(keys[key] for key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        
        # Update velocity change based on key state
        if arrow_keys_held:
            # Increase velocity change if keys are held
            velocity_change = min(velocity_change * ACCELERATION_FACTOR, MAX_VELOCITY_CHANGE)
        else:
            # Reset velocity change when keys are released
            velocity_change = BASE_VELOCITY_CHANGE
        
        # Apply velocity changes
        if keys[pygame.K_UP]:
            satellite.velocity[1] += velocity_change
        if keys[pygame.K_DOWN]:
            satellite.velocity[1] -= velocity_change
        if keys[pygame.K_RIGHT]:
            satellite.velocity[0] += velocity_change
        if keys[pygame.K_LEFT]:
            satellite.velocity[0] -= velocity_change
        
        # Store current key state
        last_key_state = keys
        
        # Update physics with time scaling
        satellite.update(TIME_STEP * time_scale)
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw Earth
        draw_earth()
        
        # Draw trajectory
        draw_trajectory(satellite.trajectory)
        
        # Draw satellite
        draw_satellite(satellite.position)
        
        # Draw information
        draw_info(time_scale, satellite.velocity, velocity_change)
        
        # Update display
        pygame.display.flip()
        
        # Cap at 60 FPS
        clock.tick(60)

if __name__ == "__main__":
    main() 