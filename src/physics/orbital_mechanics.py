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
        self.active = True
        self.current_force = 0.0
        
        # Calculate initial acceleration
        self.acceleration = self.calculate_acceleration(self.position)
    
    def calculate_acceleration(self, pos: np.ndarray) -> np.ndarray:
        """
        Calculate acceleration at a given position using Newton's law of gravitation.
        
        Args:
            pos: Position vector [x, y] in meters
            
        Returns:
            Acceleration vector [ax, ay] in m/s²
        """
        r = np.linalg.norm(pos)
        if r == 0:
            return np.zeros_like(pos)
        return -G * EARTH_MASS * pos / (r ** 3)
    
    def update(self, dt: float):
        """
        Update the position and velocity of the body using Velocity Verlet integration.
        
        Args:
            dt: Time step in seconds
        """
        if not self.active:
            return
        
        # Half-step velocity using current acceleration
        self.velocity += 0.5 * self.acceleration * dt
        
        # Full-step position
        self.position += self.velocity * dt
        
        # Calculate new acceleration
        new_acceleration = self.calculate_acceleration(self.position)
        
        # Complete velocity step using new acceleration
        self.velocity += 0.5 * new_acceleration * dt
        
        # Update acceleration
        self.acceleration = new_acceleration
        
        # Store position for trajectory
        self.trajectory.append(self.position.copy())
        
        # Limit trajectory length
        if len(self.trajectory) > 1000:
            self.trajectory.pop(0)
        
        # Update current force for display purposes
        r = np.linalg.norm(self.position)
        self.current_force = G * EARTH_MASS * self.mass / (r ** 2) 