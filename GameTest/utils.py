"""
Utility functions and helper classes
"""
import pygame
import math
import os
from typing import Tuple, List

class Vector2:
    """2D Vector class for position and velocity"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        length = self.length()
        if length > 0:
            return Vector2(self.x / length, self.y / length)
        return Vector2(0, 0)
    
    def to_tuple(self):
        return (self.x, self.y)
    
    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class Timer:
    """Simple timer class"""
    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0
        self.active = False
    
    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.active = True
    
    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.duration:
                self.active = False
                return True
        return False
    
    def is_active(self):
        return self.active
    
    def reset(self):
        self.active = False
        self.start_time = 0

class Animation:
    """Animation helper class"""
    def __init__(self, frames, frame_duration=100, loop=True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.timer = 0
        self.finished = False
    
    def update(self, dt):
        if self.finished and not self.loop:
            return
        
        self.timer += dt
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
    
    def get_current_frame(self):
        return self.frames[self.current_frame]
    
    def reset(self):
        self.current_frame = 0
        self.timer = 0
        self.finished = False

def lerp(start, end, t):
    """Linear interpolation"""
    return start + (end - start) * t

def clamp(value, min_value, max_value):
    """Clamp value between min and max"""
    return max(min_value, min(value, max_value))

def rect_collision(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """Check if two rectangles collide"""
    return rect1.colliderect(rect2)

def circle_collision(pos1: Tuple[float, float], radius1: float, 
                     pos2: Tuple[float, float], radius2: float) -> bool:
    """Check if two circles collide"""
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    distance = math.sqrt(dx**2 + dy**2)
    return distance < radius1 + radius2

def draw_text(surface, text, pos, font, color=(255, 255, 255), 
              center=False, shadow=False):
    """Draw text on surface with optional centering and shadow"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if center:
        text_rect.center = pos
    else:
        text_rect.topleft = pos
    
    if shadow:
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        surface.blit(shadow_surface, shadow_rect)
    
    surface.blit(text_surface, text_rect)
    return text_rect

def load_image(path, scale=None, colorkey=None):
    """Load an image with optional scaling and color key"""
    try:
        image = pygame.image.load(path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        if colorkey:
            image.set_colorkey(colorkey)
        return image
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        # Return a placeholder surface
        surf = pygame.Surface((32, 32))
        surf.fill((255, 0, 255))  # Magenta for missing textures
        return surf

def create_placeholder_surface(width, height, color=(255, 0, 255)):
    """Create a placeholder surface"""
    surf = pygame.Surface((width, height))
    surf.fill(color)
    return surf

def load_spritesheet(path, sprite_width, sprite_height, scale=1):
    """Load a spritesheet and return a list of frames"""
    try:
        sheet = pygame.image.load(path).convert_alpha()
    except pygame.error:
        # Create placeholder
        return [create_placeholder_surface(sprite_width * scale, sprite_height * scale)]
    
    sheet_width = sheet.get_width()
    sheet_height = sheet.get_height()
    
    frames = []
    for y in range(0, sheet_height, sprite_height):
        for x in range(0, sheet_width, sprite_width):
            frame = sheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))
            if scale != 1:
                frame = pygame.transform.scale(frame, 
                                             (sprite_width * scale, sprite_height * scale))
            frames.append(frame)
    
    return frames

def ensure_directory(path):
    """Ensure a directory exists"""
    if not os.path.exists(path):
        os.makedirs(path)

def get_distance(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """Get distance between two points"""
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def get_angle(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """Get angle from pos1 to pos2 in radians"""
    return math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])

def approach(current, target, step):
    """Move current value towards target by step amount"""
    if current < target:
        return min(current + step, target)
    elif current > target:
        return max(current - step, target)
    return current
