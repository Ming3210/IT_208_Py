"""
Magic system - Spells and spell effects
"""
import pygame
import math
import random
from config import *
from utils import Vector2

class Spell:
    def __init__(self, x, y, direction, element, caster):
        self.pos = Vector2(x, y)
        self.element = element
        self.caster = caster
        self.active = True
        self.rect = pygame.Rect(x, y, 24, 24)
        
        # Movement
        angle = 0 if direction else math.pi
        self.velocity = Vector2(math.cos(angle) * 8, 0)
        
        # Stats based on element
        self.setup_element_properties()
        
        # Lifetime
        self.lifetime = 3000  # 3 seconds
        self.spawn_time = pygame.time.get_ticks()
    
    def setup_element_properties(self):
        """Set up properties based on element type"""
        if self.element == ELEMENT_FIRE:
            self.damage = 25
            self.color = ORANGE
            self.status_effect = 'burn'
        elif self.element == ELEMENT_ICE:
            self.damage = 20
            self.color = CYAN
            self.status_effect = 'freeze'
        elif self.element == ELEMENT_LIGHTNING:
            self.damage = 30
            self.color = YELLOW
            self.status_effect = 'stun'
        elif self.element == ELEMENT_EARTH:
            self.damage = 35
            self.color = (139, 69, 19)
            self.status_effect = None
            self.velocity.x *= 0.6  # Slower but stronger
        elif self.element == ELEMENT_WIND:
            self.damage = 15
            self.color = LIGHT_GRAY
            self.status_effect = 'knockback'
            self.velocity.x *= 1.5  # Faster
    
    def update(self, dt, tiles):
        """Update spell position and check collisions"""
        # Check lifetime
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.active = False
            return
        
        # Update position
        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        
        # Check tile collision
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                self.active = False
                return
    
    def check_hit(self, target_rect):
        """Check if spell hits a target"""
        if self.active and self.rect.colliderect(target_rect):
            self.active = False
            return True
        return False
    
    def draw(self, surface, camera):
        """Draw spell"""
        if not self.active:
            return
        
        screen_pos = camera.apply(self.rect)
        
        # Draw spell projectile
        pygame.draw.circle(surface, self.color, 
                         (screen_pos.centerx, screen_pos.centery), 10)
        pygame.draw.circle(surface, WHITE, 
                         (screen_pos.centerx, screen_pos.centery), 5)
        
        # Element-specific effects
        if self.element == ELEMENT_FIRE:
            # Flickering effect
            for i in range(3):
                offset = i * 8
                alpha = 100 - i * 30
                fire_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
                pygame.draw.circle(fire_surf, (*ORANGE, alpha), (10, 10), 8 - i * 2)
                surface.blit(fire_surf, (screen_pos.x - offset, screen_pos.y))
        
        elif self.element == ELEMENT_ICE:
            # Crystal shards
            points = [
                (screen_pos.centerx, screen_pos.top),
                (screen_pos.right, screen_pos.centery),
                (screen_pos.centerx, screen_pos.bottom),
                (screen_pos.left, screen_pos.centery)
            ]
            pygame.draw.polygon(surface, CYAN, points, 2)
        
        elif self.element == ELEMENT_LIGHTNING:
            # Electric arc
            start = (screen_pos.centerx, screen_pos.centery)
            for _ in range(3):
                end_x = start[0] + random.randint(-15, 15)
                end_y = start[1] + random.randint(-15, 15)
                pygame.draw.line(surface, YELLOW, start, (end_x, end_y), 2)

class MagicSystem:
    def __init__(self):
        self.spells = []
        self.combinations = {
            ('fire', 'wind'): 'firestorm',
            ('ice', 'lightning'): 'frozen_lightning',
            ('earth', 'fire'): 'lava',
            ('wind', 'lightning'): 'thunderstorm',
            ('ice', 'water'): 'blizzard'
        }
    
    def create_spell(self, x, y, direction, element, caster):
        """Create a new spell"""
        spell = Spell(x, y, direction, element, caster)
        self.spells.append(spell)
        return spell
    
    def update(self, dt, tiles):
        """Update all spells"""
        # Remove inactive spells
        self.spells = [s for s in self.spells if s.active]
        
        # Update active spells
        for spell in self.spells:
            spell.update(dt, tiles)
    
    def check_hits(self, target_rect, caster=None):
        """Check if any spells hit a target"""
        hits = []
        for spell in self.spells:
            if spell.caster == caster and spell.check_hit(target_rect):  # Changed != to ==
                hits.append(spell)
        return hits
    
    def draw(self, surface, camera):
        """Draw all spells"""
        for spell in self.spells:
            spell.draw(surface, camera)
    
    def clear(self):
        """Clear all spells"""
        self.spells.clear()
