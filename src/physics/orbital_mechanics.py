"""Orbital mechanics calculations module."""

import numpy as np
from .constants import G, EARTH_MASS

class OrbitalBody:
    """Represents an object in orbit around Earth."""
    
    def __init__(self, position: np.ndarray, velocity: np.ndarray, mass: float = 1000.0):
        """
        Initialize an orbital body.
        
        Args:
            position: Initial position vector [x, y] in meters
            velocity: Initial velocity vector [vx, vy] in m/s
            mass: Mass of the object in kg
        """
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.mass = mass
        self.trajectory = [self.position.copy()]
    
    def update(self, dt: float):
        """
        Update the position and velocity of the body using simple Euler integration.
        
        Args:
            dt: Time step in seconds
        """
        # Calculate distance to Earth's center
        r = np.linalg.norm(self.position)
        
        # Calculate gravitational force
        force = -G * EARTH_MASS * self.mass * self.position / (r ** 3)
        
        # Calculate acceleration
        acceleration = force / self.mass
        
        # Update velocity and position (Euler integration)
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        
        # Store position for trajectory
        self.trajectory.append(self.position.copy())
        
        # Limit trajectory length to avoid memory issues
        if len(self.trajectory) > 1000:
            self.trajectory.pop(0) 