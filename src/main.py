"""Main entry point for the orbital simulation."""

import sys
import pygame
import numpy as np
from src.physics.constants import EARTH_RADIUS, G, EARTH_MASS
from src.physics.orbital_mechanics import OrbitalBody
from src.visualization.renderer import Renderer
from src.ui.control_panel import ControlPanel

def calculate_circular_orbit_velocity(radius: float) -> float:
    """Calculate velocity needed for circular orbit at given radius."""
    return np.sqrt(G * EARTH_MASS / radius)

def create_circular_orbit(altitude: float = 500_000) -> OrbitalBody:
    """
    Create an orbital body in a circular orbit at the specified altitude.
    
    Args:
        altitude: Altitude above Earth's surface in meters (default: 500 km)
        
    Returns:
        OrbitalBody instance
    """
    radius = EARTH_RADIUS + altitude
    velocity = calculate_circular_orbit_velocity(radius)
    
    # Position at the 3 o'clock position (right side of Earth)
    position = np.array([radius, 0.0])
    
    # Velocity vector perpendicular to position (for circular orbit)
    velocity_vector = np.array([0.0, velocity])
    
    return OrbitalBody(position, velocity_vector)

def create_elliptical_orbit(perigee: float = 500_000, apogee: float = 2_000_000) -> OrbitalBody:
    """
    Create an orbital body in an elliptical orbit with the specified perigee and apogee.
    
    Args:
        perigee: Closest approach to Earth's surface in meters (default: 500 km)
        apogee: Furthest distance from Earth's surface in meters (default: 2000 km)
        
    Returns:
        OrbitalBody instance
    """
    # Calculate semi-major axis
    r_p = EARTH_RADIUS + perigee  # Perigee radius
    r_a = EARTH_RADIUS + apogee   # Apogee radius
    semi_major_axis = (r_p + r_a) / 2
    
    # Start at perigee (closest approach)
    position = np.array([r_p, 0.0])
    
    # Calculate velocity at perigee (vis-viva equation)
    velocity = np.sqrt(G * EARTH_MASS * (2/r_p - 1/semi_major_axis))
    velocity_vector = np.array([0.0, velocity])
    
    return OrbitalBody(position, velocity_vector)

def main():
    """Main function to run the simulation."""
    # Initialize pygame
    pygame.init()
    
    # Create renderer
    renderer = Renderer()
    
    # Create control panel
    control_panel = ControlPanel(renderer.width, renderer.height)
    
    # Create initial satellites
    satellites = [create_circular_orbit()]
    
    # Set reset callback
    def reset_simulation():
        satellites.clear()
        satellites.append(create_circular_orbit())
    
    control_panel.set_reset_callback(reset_simulation)
    
    # Simulation timing
    clock = pygame.time.Clock()
    dt = 1.0  # Base time step in seconds
    VELOCITY_INCREMENT = 100.0 # m/s per key press for velocity adjustment
    
    # Main loop
    running = True
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_c:
                    # Add circular orbit
                    if len(satellites) < 5:  # Limit to 5 satellites
                        satellites.append(create_circular_orbit(altitude=np.random.uniform(300_000, 1_000_000)))
                elif event.key == pygame.K_e:
                    # Add elliptical orbit
                    if len(satellites) < 5:  # Limit to 5 satellites
                        satellites.append(create_elliptical_orbit())
                
                # Velocity controls for the first satellite
                elif satellites: # Ensure there is at least one satellite
                    if event.key == pygame.K_UP:
                        satellites[0].velocity[1] += VELOCITY_INCREMENT
                    elif event.key == pygame.K_DOWN:
                        satellites[0].velocity[1] -= VELOCITY_INCREMENT
                    elif event.key == pygame.K_LEFT:
                        satellites[0].velocity[0] -= VELOCITY_INCREMENT
                    elif event.key == pygame.K_RIGHT:
                        satellites[0].velocity[0] += VELOCITY_INCREMENT
            
            # Handle UI events
            control_panel.handle_event(event)
        
        # Update mouse position for UI hover effects
        mouse_pos = pygame.mouse.get_pos()
        control_panel.update(mouse_pos)
        
        # Get time scale from control panel
        time_scale = control_panel.get_time_scale()
        
        # Update physics (skip if paused)
        if time_scale > 0:
            scaled_dt = dt * time_scale
            for satellite in satellites:
                satellite.update(scaled_dt)
        
        # Render everything
        renderer.render(satellites, time_scale)
        control_panel.draw(renderer.screen)
        
        # Update display
        pygame.display.flip()
        
        # Cap at 60 FPS
        clock.tick(60)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 