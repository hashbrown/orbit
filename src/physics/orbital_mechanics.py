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
    
    def calculate_gravitational_force(self) -> tuple[np.ndarray, float]:
        """
        Calculate the gravitational force vector using Newton's law of universal gravitation.
        
        Returns:
            Tuple of (force vector [Fx, Fy] in Newtons, force magnitude in Newtons)
        """
        # Calculate distance to Earth's center
        r = np.linalg.norm(self.position)
        
        # Calculate force magnitude using F = G(M*m)/r²
        force_magnitude = G * EARTH_MASS * self.mass / (r ** 2)
        
        # Calculate force vector (pointing toward Earth's center)
        force_vector = -force_magnitude * self.position / r
        
        return force_vector, force_magnitude
    
    def update(self, dt: float):
        """
        Update the position and velocity of the body using Euler integration.
        
        Args:
            dt: Time step in seconds
        """
        if not self.active:
            return

        # Calculate acceleration (gravitational force / mass)
        force_vector, self.current_force = self.calculate_gravitational_force()
        acceleration = force_vector / self.mass
        
        # Euler integration
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        
        # Store position for trajectory
        self.trajectory.append(self.position.copy())
        
        # Limit trajectory length
        if len(self.trajectory) > 1000:
            self.trajectory.pop(0)
    
    def calculate_acceleration(self, pos: np.ndarray) -> np.ndarray:
        """Calculate acceleration at a given position."""
        r = np.linalg.norm(pos)
        return -G * EARTH_MASS * pos / (r ** 3) 