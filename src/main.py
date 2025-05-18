"""Main entry point for the orbital simulation."""

import sys
import pygame
import numpy as np
from src.physics.constants import (
    EARTH_RADIUS, G, EARTH_MASS, MOON_MASS, MOON_ORBITAL_RADIUS,
    ISS_MASS, ISS_ORBITAL_RADIUS, TIME_SCALE, SIMULATION_DURATION
)
from src.physics.orbital_mechanics import OrbitalBody
from src.visualization.renderer import Renderer
from src.ui.control_panel import ControlPanel

def calculate_circular_orbit_velocity(radius: float, central_mass: float = EARTH_MASS) -> float:
    """Calculate velocity needed for circular orbit at given radius."""
    return np.sqrt(G * central_mass / radius)

def create_moon() -> OrbitalBody:
    """Create the Moon in its orbit around Earth."""
    velocity = calculate_circular_orbit_velocity(MOON_ORBITAL_RADIUS)
    position = np.array([MOON_ORBITAL_RADIUS, 0.0])
    velocity_vector = np.array([0.0, velocity])
    return OrbitalBody(position, velocity_vector, mass=MOON_MASS)

def create_iss() -> OrbitalBody:
    """Create the ISS in its orbit around Earth."""
    velocity = calculate_circular_orbit_velocity(ISS_ORBITAL_RADIUS)
    position = np.array([ISS_ORBITAL_RADIUS, 0.0])
    velocity_vector = np.array([0.0, velocity])
    return OrbitalBody(position, velocity_vector, mass=ISS_MASS)

def main():
    """Main function to run the simulation."""
    # Initialize pygame
    pygame.init()
    
    # Create renderer
    renderer = Renderer()
    
    # Create control panel
    control_panel = ControlPanel(renderer.width, renderer.height)
    
    # Create Moon and ISS
    celestial_bodies = [create_moon(), create_iss()]
    
    # Set reset callback
    def reset_simulation():
        celestial_bodies.clear()
        celestial_bodies.extend([create_moon(), create_iss()])
    
    control_panel.set_reset_callback(reset_simulation)
    
    # Simulation timing
    clock = pygame.time.Clock()
    dt = 0.1  # Base time step in seconds (reduced for stability)
    control_panel.set_time_scale(TIME_SCALE)  # 24 hours in 1 minute
    
    # Main loop
    running = True
    simulation_time = 0.0  # Track total simulation time
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
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
            simulation_time += scaled_dt
            
            # Stop after 24 hours of simulation time
            if simulation_time >= SIMULATION_DURATION:
                time_scale = 0
                control_panel.set_time_scale(0)  # Pause the simulation
            
            for body in celestial_bodies:
                body.update(scaled_dt)
        
        # Get visibility state
        show_moon, show_iss = control_panel.get_visibility()
        
        # Create list of visible bodies
        visible_bodies = []
        if show_moon:
            visible_bodies.append(celestial_bodies[0])
        if show_iss:
            visible_bodies.append(celestial_bodies[1])
        
        # Render everything
        renderer.render(visible_bodies, time_scale)
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