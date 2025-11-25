"""
Boss battles
"""
import pygame
import random
from enemy import Enemy
from config import *
from utils import Timer

class Boss(Enemy):
    def __init__(self, x, y, boss_type='forest_guardian'):
        self.boss_type = boss_type
        super().__init__(x, y, boss_type)
        
        self.phase = 1
        self.max_phases = 3
        self.phase_threshold = self.max_hp // self.max_phases
        
        # Boss-specific timers
        self.special_attack_timer = Timer(5000)
        self.invulnerable = False
        self.invulnerable_timer = Timer(2000)
    
    def setup_enemy_stats(self):
        """Setup boss stats"""
        if self.boss_type == 'forest_guardian':
            self.max_hp = 500
            self.hp = self.max_hp
            self.damage = 30
            self.speed = 1
            self.detection_range = 800
            self.attack_range = 100
            self.attack_cooldown = 1200
            self.xp_value = 500
            self.width = 128
            self.height = 128
        
        elif self.boss_type == 'crystal_golem':
            self.max_hp = 800
            self.hp = self.max_hp
            self.damage = 40
            self.speed = 0.5
            self.detection_range = 1000
            self.attack_range = 80
            self.attack_cooldown = 1500
            self.xp_value = 800
            self.width = 96
            self.height = 128
            self.defense = 0.5  # Takes half damage
        
        elif self.boss_type == 'shadow_lord':
            self.max_hp = 1000
            self.hp = self.max_hp
            self.damage = 50
            self.speed = 2
            self.detection_range = 1200
            self.attack_range = 400
            self.attack_cooldown = 800
            self.xp_value = 1500
            self.width = 128
            self.height = 128
            self.can_teleport = True
    
    def update(self, dt, player, tiles):
        """Update boss with phase management"""
        # Check phase transitions
        current_phase = (self.max_hp - self.hp) // self.phase_threshold + 1
        if current_phase > self.phase and current_phase <= self.max_phases:
            self.phase = current_phase
            self.on_phase_change()
        
        # Update special attack timer
        if self.special_attack_timer.update():
            self.use_special_attack(player)
            self.special_attack_timer.start()
        
        # Update invulnerability
        self.invulnerable_timer.update()
        if not self.invulnerable_timer.is_active():
            self.invulnerable = False
        
        # Regular update
        super().update(dt, player, tiles)
    
    def on_phase_change(self):
        """Handle phase transitions"""
        if self.boss_type == 'forest_guardian':
            # Summon adds
            self.speed += 0.5
            self.attack_cooldown = max(600, self.attack_cooldown - 200)
        
        elif self.boss_type == 'crystal_golem':
            # Become invulnerable briefly
            self.invulnerable = True
            self.invulnerable_timer.start()
            # Increase defense
            self.defense = max(0.2, self.defense - 0.1)
        
        elif self.boss_type == 'shadow_lord':
            # Increase speed and damage
            self.speed += 0.5
            self.damage += 10
    
    def use_special_attack(self, player):
        """Execute special attack based on boss type"""
        if self.boss_type == 'forest_guardian':
            # Root attack - slows player
            return 'root_attack'
        
        elif self.boss_type == 'crystal_golem':
            # Ground slam
            return 'ground_slam'
        
        elif self.boss_type == 'shadow_lord':
            # Shadow clone or teleport
            if random.random() < 0.5:
                return 'teleport'
            else:
                return 'shadow_clone'
        
        return None
    
    def take_damage(self, damage):
        """Take damage with boss-specific mechanics"""
        if self.invulnerable:
            return False
        
        # Apply defense if applicable
        if hasattr(self, 'defense'):
            damage *= (1 - self.defense)
        
        return super().take_damage(int(damage))
    
    def draw(self, surface, camera, assets):
        """Draw boss with special effects"""
        screen_pos = camera.apply(self.rect)
        
        # Get boss sprite
        sprite = assets.get_image('bosses', self.boss_type)
        
        # Flip if facing left
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        # Flash when hit
        if self.hit_timer.is_active():
            sprite = sprite.copy()
            sprite.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_ADD)
        
        # Invulnerable effect
        if self.invulnerable:
            sprite = sprite.copy()
            sprite.fill((200, 200, 255, 128), special_flags=pygame.BLEND_RGBA_ADD)
        
        surface.blit(sprite, screen_pos)
        
        # Draw boss health bar at top of screen
        self.draw_boss_health_bar(surface)
    
    def draw_boss_health_bar(self, surface):
        """Draw boss health bar at top of screen"""
        bar_width = 600
        bar_height = 30
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 20
        
        # Background
        pygame.draw.rect(surface, DARK_GRAY, 
                       (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(surface, BLACK, 
                       (bar_x, bar_y, bar_width, bar_height))
        
        # Health
        health_ratio = self.hp / self.max_hp
        health_width = int(health_ratio * bar_width)
        
        # Color changes based on health
        if health_ratio > 0.6:
            color = GREEN
        elif health_ratio > 0.3:
            color = YELLOW
        else:
            color = RED
        
        pygame.draw.rect(surface, color, 
                       (bar_x, bar_y, health_width, bar_height))
        
        # Phase markers
        for i in range(1, self.max_phases):
            marker_x = bar_x + (bar_width // self.max_phases) * i
            pygame.draw.line(surface, WHITE, 
                           (marker_x, bar_y), (marker_x, bar_y + bar_height), 2)
        
        # Boss name
        from assets_manager import assets
        font = assets.get_font('medium')
        name_text = f"{self.boss_type.replace('_', ' ').title()} - Phase {self.phase}"
        text_surface = font.render(name_text, True, WHITE)
        text_rect = text_surface.get_rect(centerx=SCREEN_WIDTH // 2, bottom=bar_y - 5)
        surface.blit(text_surface, text_rect)
