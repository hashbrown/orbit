"""Visualization module for the orbital mechanics simulation."""

import pygame
import numpy as np
from typing import List, Tuple
from src.physics.orbital_mechanics import OrbitalBody
from src.physics.constants import (
    EARTH_RADIUS, SCALE_FACTOR, MOON_SCALE_FACTOR, MOON_RADIUS,
    MOON_ORBITAL_RADIUS, ISS_ORBITAL_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
)

class Renderer:
    """Renders the orbital simulation using Pygame."""
    
    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
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
        pygame.display.set_caption("Earth-Moon-ISS Orbital Simulation")
        
        # Colors
        self.bg_color = (0, 0, 0)  # Black background
        self.earth_color = (100, 149, 237)  # Cornflower blue for Earth
        self.moon_color = (200, 200, 200)  # Light gray for Moon
        self.iss_color = (255, 255, 255)  # White for ISS
        self.trajectory_color = (50, 50, 50)  # Dark gray for trajectories
        self.line_color = (40, 40, 40)  # Dark gray for connecting lines
        
        # Center of the screen (Earth's position)
        self.center_x = width // 2
        self.center_y = height // 2
        
        # Radii in pixels on screen
        # Make Earth small but visible
        earth_scaled_radius = EARTH_RADIUS * SCALE_FACTOR
        self.earth_radius_px = max(4, min(6, int(earth_scaled_radius)))
        
        # Scale Moon relative to Earth but ensure visibility
        moon_scaled_radius = MOON_RADIUS * MOON_SCALE_FACTOR
        self.moon_radius_px = max(3, min(4, int(moon_scaled_radius)))
        
        # ISS as a small dot
        self.iss_radius_px = 2
        
        # Font for displaying information
        self.font = pygame.font.SysFont("Arial", 16)
        self.small_font = pygame.font.SysFont("Arial", 12)
    
    def world_to_screen(self, position: np.ndarray, is_moon: bool = False) -> Tuple[int, int]:
        """
        Convert world coordinates to screen coordinates.
        
        Args:
            position: Position vector [x, y] in meters
            is_moon: Whether this position is for the Moon (uses different scale)
            
        Returns:
            Tuple of (screen_x, screen_y) in pixels
        """
        scale = MOON_SCALE_FACTOR if is_moon else SCALE_FACTOR
        screen_x = self.center_x + int(position[0] * scale)
        screen_y = self.center_y - int(position[1] * scale)  # Y is inverted in screen coordinates
        return (screen_x, screen_y)
    
    def draw_earth(self):
        """Draw Earth at the center of the screen."""
        # Draw Moon's orbital path
        moon_orbit_radius = int(MOON_ORBITAL_RADIUS * MOON_SCALE_FACTOR)
        pygame.draw.circle(
            self.screen,
            (30, 30, 30),  # Very dark gray
            (self.center_x, self.center_y),
            moon_orbit_radius,
            1  # Line width of 1 pixel
        )
        
        # Draw Earth
        pygame.draw.circle(
            self.screen,
            self.earth_color,
            (self.center_x, self.center_y),
            self.earth_radius_px
        )
    
    def draw_crosshair(self, pos: Tuple[int, int], size: int = 10, color: Tuple[int, int, int] = (100, 100, 100)):
        """Draw a crosshair at the specified position."""
        x, y = pos
        # Horizontal line
        pygame.draw.line(self.screen, color, (x - size, y), (x + size, y))
        # Vertical line
        pygame.draw.line(self.screen, color, (x, y - size), (x, y + size))
    
    def draw_connecting_line(self, body_pos: Tuple[int, int], color: Tuple[int, int, int], distance_km: float):
        """Draw a line connecting Earth to a celestial body with distance marker."""
        # Draw line from Earth center to body
        pygame.draw.line(
            self.screen,
            self.line_color,
            (self.center_x, self.center_y),
            body_pos,
            1
        )
        
        # Calculate midpoint for distance label
        mid_x = (self.center_x + body_pos[0]) // 2
        mid_y = (self.center_y + body_pos[1]) // 2
        
        # Draw distance label
        distance_text = f"{distance_km:,.0f} km"
        text_surface = self.small_font.render(distance_text, True, color)
        text_rect = text_surface.get_rect(center=(mid_x, mid_y - 10))
        self.screen.blit(text_surface, text_rect)
    
    def draw_celestial_body(self, body: OrbitalBody, index: int):
        """
        Draw a celestial body and its trajectory.
        
        Args:
            body: The orbital body to draw
            index: Index in the visible bodies list (not used for identification)
        """
        if not body.active:
            return
        
        # Determine if it's the Moon based on mass
        is_moon = body.mass > 1e20
        
        # Draw trajectory
        if len(body.trajectory) > 1:
            points = [self.world_to_screen(pos, is_moon) for pos in body.trajectory]
            pygame.draw.lines(self.screen, self.trajectory_color, False, points, 1)
        
        # Get screen position
        body_pos = self.world_to_screen(body.position, is_moon)
        color = self.moon_color if is_moon else self.iss_color
        radius = self.moon_radius_px if is_moon else self.iss_radius_px
        
        # Draw connecting line with distance
        distance = np.linalg.norm(body.position) / 1000.0  # Convert to km
        self.draw_connecting_line(body_pos, color, distance)
        
        # Draw the body
        pygame.draw.circle(self.screen, color, body_pos, radius)
        
        # Draw label
        label = "Moon" if is_moon else "ISS"
        text_surface = self.font.render(label, True, color)
        text_rect = text_surface.get_rect(center=(body_pos[0], body_pos[1] - radius - 15))
        self.screen.blit(text_surface, text_rect)
    
    def draw_info(self, bodies: List[OrbitalBody], time_scale: float):
        """
        Draw simulation information.
        
        Args:
            bodies: List of orbital bodies [Moon, ISS]
            time_scale: Current time scale of the simulation
        """
        info_text = [f"Time Scale: {time_scale/3600:.1f} hours/sec"]
        
        # Add body info if they're visible
        for body in bodies:
            # Calculate distance and velocity
            altitude = (np.linalg.norm(body.position) - EARTH_RADIUS) / 1000.0  # km
            velocity = np.linalg.norm(body.velocity) * 3.6  # km/h
            
            # Determine if it's the Moon or ISS based on mass
            if body.mass > 1e20:  # Moon
                info_text.extend([
                    "Moon:",
                    f"  Altitude: {altitude:.1f} km",
                    f"  Velocity: {velocity:.1f} km/h"
                ])
            else:  # ISS
                info_text.extend([
                    "ISS:",
                    f"  Altitude: {altitude:.1f} km",
                    f"  Velocity: {velocity:.1f} km/h"
                ])
        
        # Display info
        for i, text in enumerate(info_text):
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, 10 + i * 20))
    
    def render(self, bodies: List[OrbitalBody], time_scale: float = 1.0):
        """
        Render the current state of the simulation.
        
        Args:
            bodies: List of orbital bodies to render [Moon, ISS]
            time_scale: Current time scale of the simulation
        """
        # Fill background
        self.screen.fill(self.bg_color)
        
        # Draw Earth
        self.draw_earth()
        
        # Draw Moon and ISS
        for i, body in enumerate(bodies):
            self.draw_celestial_body(body, i)
        
        # Draw information
        self.draw_info(bodies, time_scale)
        
        # Update display
        # pygame.display.flip() 