"""
Particle system for visual effects
"""
import pygame
import random
import math
from config import *

class Particle:
    def __init__(self, pos, velocity, color, size, lifetime, gravity=0):
        self.x = pos[0]
        self.y = pos[1]
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.color = color
        self.size = size
        self.max_size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.gravity = gravity
        self.alpha = 255
    
    def update(self, dt):
        """Update particle physics"""
        dt_seconds = dt / 1000.0
        
        # Update position
        self.x += self.vx * dt_seconds * 60
        self.y += self.vy * dt_seconds * 60
        
        # Apply gravity
        self.vy += self.gravity * dt_seconds * 60
        
        # Update lifetime
        self.lifetime -= dt
        
        # Fade out
        life_ratio = self.lifetime / self.max_lifetime
        self.alpha = int(255 * life_ratio)
        self.size = self.max_size * life_ratio
        
        return self.lifetime > 0
    
    def draw(self, surface, camera):
        """Draw particle"""
        if self.size < 1:
            return
        
        screen_pos = camera.apply_pos((self.x, self.y))
        
        # Create surface with alpha
        particle_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        
        # Draw particle (circle)
        color_with_alpha = (*self.color[:3], self.alpha)
        pygame.draw.circle(particle_surface, color_with_alpha, 
                         (int(self.size), int(self.size)), int(self.size))
        
        surface.blit(particle_surface, 
                    (screen_pos[0] - self.size, screen_pos[1] - self.size))

class ParticleEmitter:
    def __init__(self, pos):
        self.pos = pos
        self.particles = []
    
    def emit(self, count, color, size_range=(2, 5), speed_range=(1, 3), 
             lifetime_range=(500, 1000), spread=360, direction=0, gravity=0):
        """Emit particles"""
        for _ in range(count):
            angle = math.radians(direction + random.uniform(-spread/2, spread/2))
            speed = random.uniform(*speed_range)
            
            velocity = (
                math.cos(angle) * speed,
                math.sin(angle) * speed
            )
            
            size = random.uniform(*size_range)
            lifetime = random.uniform(*lifetime_range)
            
            particle = Particle(self.pos, velocity, color, size, lifetime, gravity)
            self.particles.append(particle)
    
    def update(self, dt):
        """Update all particles"""
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def draw(self, surface, camera):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(surface, camera)
    
    def set_position(self, pos):
        """Update emitter position"""
        self.pos = pos

class ParticleSystem:
    """Global particle system manager"""
    def __init__(self):
        self.emitters = []
    
    def create_emitter(self, pos):
        """Create a new emitter"""
        emitter = ParticleEmitter(pos)
        self.emitters.append(emitter)
        return emitter
    
    def create_explosion(self, pos, color, count=20):
        """Create explosion effect"""
        emitter = self.create_emitter(pos)
        emitter.emit(count, color, size_range=(3, 8), speed_range=(2, 6),
                    lifetime_range=(300, 800), spread=360, gravity=0.2)
        return emitter
    
    def create_magic_cast(self, pos, element):
        """Create magic casting effect"""
        colors = {
            ELEMENT_FIRE: ORANGE,
            ELEMENT_ICE: CYAN,
            ELEMENT_LIGHTNING: YELLOW,
            ELEMENT_EARTH: (139, 69, 19),  # Brown
            ELEMENT_WIND: LIGHT_GRAY
        }
        color = colors.get(element, WHITE)
        
        emitter = self.create_emitter(pos)
        emitter.emit(15, color, size_range=(2, 4), speed_range=(1, 2),
                    lifetime_range=(400, 700), spread=360)
        return emitter
    
    def create_spell_trail(self, pos, element):
        """Create spell projectile trail"""
        colors = {
            ELEMENT_FIRE: ORANGE,
            ELEMENT_ICE: CYAN,
            ELEMENT_LIGHTNING: YELLOW,
            ELEMENT_EARTH: (139, 69, 19),
            ELEMENT_WIND: LIGHT_GRAY
        }
        color = colors.get(element, WHITE)
        
        emitter = self.create_emitter(pos)
        emitter.emit(3, color, size_range=(2, 4), speed_range=(0.5, 1),
                    lifetime_range=(200, 400), spread=60, direction=180)
        return emitter
    
    def create_impact(self, pos, element):
        """Create spell impact effect"""
        colors = {
            ELEMENT_FIRE: ORANGE,
            ELEMENT_ICE: CYAN,
            ELEMENT_LIGHTNING: YELLOW,
            ELEMENT_EARTH: (139, 69, 19),
            ELEMENT_WIND: LIGHT_GRAY
        }
        color = colors.get(element, WHITE)
        
        emitter = self.create_emitter(pos)
        emitter.emit(25, color, size_range=(4, 10), speed_range=(3, 7),
                    lifetime_range=(500, 1000), spread=360, gravity=0.3)
        return emitter
    
    def create_heal_effect(self, pos):
        """Create healing effect"""
        emitter = self.create_emitter(pos)
        emitter.emit(20, GREEN, size_range=(3, 6), speed_range=(1, 3),
                    lifetime_range=(600, 1200), spread=360, direction=270, gravity=-0.1)
        return emitter
    
    def update(self, dt):
        """Update all emitters"""
        # Remove empty emitters
        self.emitters = [e for e in self.emitters if len(e.particles) > 0]
        
        # Update remaining emitters
        for emitter in self.emitters:
            emitter.update(dt)
    
    def draw(self, surface, camera):
        """Draw all particles"""
        for emitter in self.emitters:
            emitter.draw(surface, camera)
    
    def clear(self):
        """Clear all particles"""
        self.emitters.clear()
