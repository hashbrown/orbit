"""UI controls for the orbital simulation."""

import pygame
from typing import Tuple, Dict, Any, Callable
from pygame.rect import Rect

class Button:
    """Simple button class for UI controls."""
    
    def __init__(self, 
                rect: Rect, 
                text: str, 
                callback: Callable[[], None], 
                color: Tuple[int, int, int] = (100, 100, 200),
                hover_color: Tuple[int, int, int] = (150, 150, 250),
                text_color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Initialize a button.
        
        Args:
            rect: The button's position and size
            text: Text to display on the button
            callback: Function to call when button is clicked
            color: Button color
            hover_color: Button color when hovered
            text_color: Text color
        """
        self.rect = rect
        self.text = text
        self.callback = callback
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        self.font = pygame.font.SysFont("Arial", 16)
    
    def draw(self, screen: pygame.Surface):
        """Draw the button."""
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def update(self, mouse_pos: Tuple[int, int]) -> bool:
        """
        Update button state based on mouse position.
        
        Args:
            mouse_pos: Current mouse position (x, y)
            
        Returns:
            True if mouse is hovering over button
        """
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse events.
        
        Args:
            event: Pygame event
            
        Returns:
            True if button was clicked
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                self.callback()
                return True
        return False

class ControlPanel:
    """Control panel for the orbital simulation."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize the control panel.
        
        Args:
            screen_width: Width of the screen
            screen_height: Height of the screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons = []
        self.time_scales = [1.0, 2.0, 5.0, 10.0]
        self.current_time_scale_index = 0
        
        # State
        self.paused = False
        
        # Create buttons
        self._create_buttons()
    
    def _create_buttons(self):
        """Create control buttons."""
        button_width = 120
        button_height = 30
        button_spacing = 10
        
        # Starting coordinates for the first button (bottom left corner)
        x = 10
        y = self.screen_height - button_height - 10
        
        # Pause/Play button
        self.buttons.append(Button(
            Rect(x, y, button_width, button_height),
            "Pause" if not self.paused else "Play",
            self._toggle_pause
        ))
        
        # Time scale button
        x += button_width + button_spacing
        self.buttons.append(Button(
            Rect(x, y, button_width, button_height),
            f"Speed: {self.time_scales[self.current_time_scale_index]}x",
            self._cycle_time_scale
        ))
        
        # Reset button
        x += button_width + button_spacing
        self.buttons.append(Button(
            Rect(x, y, button_width, button_height),
            "Reset",
            self._reset_simulation
        ))
    
    def _toggle_pause(self):
        """Toggle the pause state."""
        self.paused = not self.paused
        self.buttons[0].text = "Play" if self.paused else "Pause"
    
    def _cycle_time_scale(self):
        """Cycle through time scales."""
        self.current_time_scale_index = (self.current_time_scale_index + 1) % len(self.time_scales)
        self.buttons[1].text = f"Speed: {self.time_scales[self.current_time_scale_index]}x"
    
    def _reset_simulation(self):
        """Reset the simulation (callback will be set by main.py)"""
        pass
    
    def set_reset_callback(self, callback: Callable[[], None]):
        """Set the callback for the reset button."""
        self.buttons[2].callback = callback
    
    def draw(self, screen: pygame.Surface):
        """Draw the control panel."""
        for button in self.buttons:
            button.draw(screen)
    
    def update(self, mouse_pos: Tuple[int, int]):
        """Update button states based on mouse position."""
        for button in self.buttons:
            button.update(mouse_pos)
    
    def handle_event(self, event: pygame.event.Event):
        """Handle pygame events."""
        for button in self.buttons:
            if button.handle_event(event):
                return True
        return False
    
    def get_time_scale(self) -> float:
        """Get the current time scale."""
        if self.paused:
            return 0.0
        return self.time_scales[self.current_time_scale_index] 