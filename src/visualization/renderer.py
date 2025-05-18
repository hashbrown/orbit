"""Visualization module for the orbital mechanics simulation."""

import pygame
import numpy as np
from typing import List, Tuple
from src.physics.orbital_mechanics import OrbitalBody
from src.physics.constants import EARTH_RADIUS, SCALE_FACTOR

class Renderer:
    """Renders the orbital simulation using Pygame."""
    
    def __init__(self, width: int = 1200, height: int = 800):
        """
        Initialize the renderer.
        
        Args:
            width: Screen width in pixels
            height: Screen height in pixels
        """
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Orbital Mechanics Simulation")
        
        # Colors
        self.bg_color = (0, 0, 0)  # Black background
        self.earth_color = (0, 100, 200)  # Blue for Earth
        self.satellite_color = (255, 100, 100)  # Red for satellites
        self.trajectory_color = (50, 150, 50)  # Green for trajectories
        
        # Center of the screen (Earth's position)
        self.center_x = width // 2
        self.center_y = height // 2
        
        # Earth radius in pixels on screen
        self.earth_radius_px = int(EARTH_RADIUS * SCALE_FACTOR)
        
        # Font for displaying information
        self.font = pygame.font.SysFont("Arial", 16)
    
    def world_to_screen(self, position: np.ndarray) -> Tuple[int, int]:
        """
        Convert world coordinates to screen coordinates.
        
        Args:
            position: Position vector [x, y] in meters
            
        Returns:
            Tuple of (screen_x, screen_y) in pixels
        """
        screen_x = self.center_x + int(position[0] * SCALE_FACTOR)
        screen_y = self.center_y - int(position[1] * SCALE_FACTOR)  # Y is inverted in screen coordinates
        return (screen_x, screen_y)
    
    def draw_earth(self):
        """Draw Earth at the center of the screen."""
        pygame.draw.circle(
            self.screen,
            self.earth_color,
            (self.center_x, self.center_y),
            self.earth_radius_px
        )
    
    def draw_satellite(self, satellite: OrbitalBody):
        """
        Draw a satellite and its trajectory.
        
        Args:
            satellite: The orbital body to draw
        """
        if not satellite.active:
            return
            
        # Draw trajectory
        if len(satellite.trajectory) > 1:
            points = [self.world_to_screen(pos) for pos in satellite.trajectory]
            pygame.draw.lines(self.screen, self.trajectory_color, False, points, 1)
        
        # Draw satellite (5 pixel radius)
        sat_pos = self.world_to_screen(satellite.position)
        pygame.draw.circle(self.screen, self.satellite_color, sat_pos, 5)
    
    def draw_info(self, satellites: List[OrbitalBody], time_scale: float):
        """
        Draw simulation information.
        
        Args:
            satellites: List of orbital bodies
            time_scale: Current time scale of the simulation
        """
        if not satellites:
            return
            
        # Get the first satellite for display
        sat = satellites[0]
        
        # Calculate altitude
        altitude = np.linalg.norm(sat.position) - EARTH_RADIUS
        altitude_km = altitude / 1000.0  # Convert to km
        
        # Calculate velocity
        velocity = np.linalg.norm(sat.velocity)
        velocity_kmh = velocity * 3.6  # Convert to km/h
        
        # Display info
        info_text = [
            f"Altitude: {altitude_km:.1f} km",
            f"Velocity: {velocity_kmh:.1f} km/h",
            f"Time Scale: {time_scale}x"
        ]
        
        for i, text in enumerate(info_text):
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, 10 + i * 20))
    
    def render(self, satellites: List[OrbitalBody], time_scale: float = 1.0):
        """
        Render the current state of the simulation.
        
        Args:
            satellites: List of orbital bodies to render
            time_scale: Current time scale of the simulation
        """
        # Fill background
        self.screen.fill(self.bg_color)
        
        # Draw Earth
        self.draw_earth()
        
        # Draw satellites and trajectories
        for sat in satellites:
            self.draw_satellite(sat)
        
        # Draw information
        self.draw_info(satellites, time_scale)
        
        # Update display
        # pygame.display.flip() 