"""
Camera system for smooth following and screen shake
"""
import pygame
from config import *
from utils import lerp, clamp
import random

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        
        # Boundaries
        self.min_x = 0
        self.min_y = 0
        self.max_x = width
        self.max_y = height
        
        # Screen shake
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0
    
    def set_bounds(self, min_x, min_y, max_x, max_y):
        """Set camera boundaries based on level size"""
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max(max_x - SCREEN_WIDTH, min_x)
        self.max_y = max(max_y - SCREEN_HEIGHT, min_y)
    
    def follow(self, target_rect, smooth=True):
        """Follow a target (usually the player)"""
        # Center camera on target
        self.target_x = target_rect.centerx - SCREEN_WIDTH // 2
        self.target_y = target_rect.centery - SCREEN_HEIGHT // 2
        
        # Apply deadzone
        if abs(self.target_x - self.x) < CAMERA_DEADZONE_X:
            self.target_x = self.x
        if abs(self.target_y - self.y) < CAMERA_DEADZONE_Y:
            self.target_y = self.y
        
        # Smooth or instant follow
        if smooth:
            self.x = lerp(self.x, self.target_x, CAMERA_SPEED)
            self.y = lerp(self.y, self.target_y, CAMERA_SPEED)
        else:
            self.x = self.target_x
            self.y = self.target_y
        
        # Clamp to boundaries
        self.x = clamp(self.x, self.min_x, self.max_x)
        self.y = clamp(self.y, self.min_y, self.max_y)
    
    def update(self, dt):
        """Update camera effects"""
        # Update screen shake
        if self.shake_duration > 0:
            self.shake_duration -= dt
            self.shake_offset_x = random.uniform(-self.shake_intensity, self.shake_intensity)
            self.shake_offset_y = random.uniform(-self.shake_intensity, self.shake_intensity)
            
            if self.shake_duration <= 0:
                self.shake_offset_x = 0
                self.shake_offset_y = 0
                self.shake_intensity = 0
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0
    
    def shake(self, intensity=5, duration=200):
        """Trigger screen shake effect"""
        self.shake_intensity = intensity
        self.shake_duration = duration
    
    def apply(self, entity_rect):
        """Apply camera offset to an entity's rect for rendering"""
        return pygame.Rect(
            entity_rect.x - self.x + self.shake_offset_x,
            entity_rect.y - self.y + self.shake_offset_y,
            entity_rect.width,
            entity_rect.height
        )
    
    def apply_pos(self, pos):
        """Apply camera offset to a position tuple"""
        return (
            pos[0] - self.x + self.shake_offset_x,
            pos[1] - self.y + self.shake_offset_y
        )
    
    def get_offset(self):
        """Get camera offset as tuple"""
        return (int(self.x), int(self.y))
    
    def is_visible(self, rect):
        """Check if a rect is visible in the camera view"""
        camera_rect = pygame.Rect(self.x, self.y, SCREEN_WIDTH, SCREEN_HEIGHT)
        return camera_rect.colliderect(rect)
