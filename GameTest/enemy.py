"""
Enemy AI and behaviors
"""
import pygame
import random
import math
from config import *
from utils import Vector2, Timer, get_distance

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type='slime'):
        super().__init__()
        
        self.pos = Vector2(x, y)
        self.enemy_type = enemy_type
        self.setup_enemy_stats()
        
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.velocity = Vector2(0, 0)
        
        # AI State
        self.state = 'patrol'  # patrol, chase, attack, retreat
        self.facing_right = True
        self.on_ground = False
        
        # Patrol
        self.patrol_start = x
        self.patrol_range = 200
        self.patrol_speed = 1
        
        # Combat
        self.attack_timer = Timer(self.attack_cooldown)
        self.hit_timer = Timer(200)
        
        # Animation
        self.animation_frame = 0
        self.animation_timer = 0
        
        # Drops
        self.setup_drops()
    
    def setup_enemy_stats(self):
        """Setup stats based on enemy type"""
        if self.enemy_type == 'slime':
            self.max_hp = 30
            self.hp = self.max_hp
            self.damage = 10
            self.speed = 1.5
            self.detection_range = 300
            self.attack_range = 50
            self.attack_cooldown = 1500
            self.xp_value = 15
            self.width = 32
            self.height = 24
        
        elif self.enemy_type == 'skeleton':
            self.max_hp = 50
            self.hp = self.max_hp
            self.damage = 15
            self.speed = 2
            self.detection_range = 400
            self.attack_range = 60
            self.attack_cooldown = 1000
            self.xp_value = 25
            self.width = 48
            self.height = 64
        
        elif self.enemy_type == 'shadow_beast':
            self.max_hp = 70
            self.hp = self.max_hp
            self.damage = 20
            self.speed = 3
            self.detection_range = 500
            self.attack_range = 70
            self.attack_cooldown = 800
            self.xp_value = 40
            self.width = 64
            self.height = 48
        
        elif self.enemy_type == 'corrupted_mage':
            self.max_hp = 40
            self.hp = self.max_hp
            self.damage = 25
            self.speed = 1
            self.detection_range = 600
            self.attack_range = 400  # Ranged
            self.attack_cooldown = 2000
            self.xp_value = 50
            self.can_cast_spells = True
            self.width = 48
            self.height = 64
        
        elif self.enemy_type == 'bat':
            self.max_hp = 20
            self.hp = self.max_hp
            self.damage = 8
            self.speed = 2.5
            self.detection_range = 400
            self.attack_range = 40
            self.attack_cooldown = 600
            self.xp_value = 12
            self.can_fly = True
            self.width = 32
            self.height = 24
        
        else:
            # Default
            self.max_hp = 30
            self.hp = 30
            self.damage = 10
            self.speed = 1.5
            self.detection_range = 300
            self.attack_range = 50
            self.attack_cooldown = 1000
            self.xp_value = 10
            self.width = 32
            self.height = 32
    
    def setup_drops(self):
        """Setup drop table"""
        self.drops = []
        
        # Gold drop (guaranteed)
        gold_amount = random.randint(5, 15) * (1 if self.enemy_type == 'slime' else 2)
        self.drops.append(('gold', gold_amount))
        
        # Chance for health potion
        if random.random() < 0.3:
            self.drops.append(('health_potion', 1))
        
        # Chance for mana potion
        if random.random() < 0.2:
            self.drops.append(('mana_potion', 1))
    
    def update(self, dt, player, tiles):
        """Update enemy AI and physics"""
        # Update timers
        self.attack_timer.update()
        self.hit_timer.update()
        
        # AI behavior
        distance_to_player = get_distance(
            (self.rect.centerx, self.rect.centery),
            (player.rect.centerx, player.rect.centery)
        )
        
        # State machine
        if distance_to_player < self.detection_range:
            if distance_to_player < self.attack_range:
                self.state = 'attack'
            else:
                self.state = 'chase'
        else:
            self.state = 'patrol'
        
        # Execute state behavior
        if self.state == 'patrol':
            self.patrol()
        elif self.state == 'chase':
            self.chase(player)
        elif self.state == 'attack':
            self.attack_player(player)
        
        # Apply gravity (if not flying)
        if not hasattr(self, 'can_fly') or not self.can_fly:
            self.velocity.y += GRAVITY
            self.velocity.y = min(self.velocity.y, MAX_FALL_SPEED)
        
        # Update position
        self.pos.x += self.velocity.x
        self.rect.x = int(self.pos.x)
        self.handle_collision_x(tiles)
        
        self.pos.y += self.velocity.y
        self.rect.y = int(self.pos.y)
        self.handle_collision_y(tiles)
        
        # Update animation
        self.animation_timer += dt
        if self.animation_timer >= 200:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
    
    def patrol(self):
        """Patrol behavior"""
        # Move back and forth
        if self.rect.x < self.patrol_start - self.patrol_range:
            self.facing_right = True
        elif self.rect.x > self.patrol_start + self.patrol_range:
            self.facing_right = False
        
        self.velocity.x = self.patrol_speed if self.facing_right else -self.patrol_speed
    
    def chase(self, player):
        """Chase player"""
        if player.rect.centerx > self.rect.centerx:
            self.velocity.x = self.speed
            self.facing_right = True
        else:
            self.velocity.x = -self.speed
            self.facing_right = False
        
        # Flying enemies can move vertically
        if hasattr(self, 'can_fly') and self.can_fly:
            if player.rect.centery > self.rect.centery:
                self.velocity.y = self.speed
            else:
                self.velocity.y = -self.speed
    
    def attack_player(self, player):
        """Attack behavior"""
        self.velocity.x = 0
        
        if not self.attack_timer.is_active():
            # Face player
            self.facing_right = player.rect.centerx > self.rect.centerx
            
            # Attack
            if self.rect.colliderect(player.rect):
                player.take_damage(self.damage)
                self.attack_timer.start()
                return True
        
        return False
    
    def take_damage(self, damage):
        """Take damage"""
        self.hp -= damage
        self.hit_timer.start()
        
        if self.hp <= 0:
            return True  # Dead
        return False
    
    def handle_collision_x(self, tiles):
        """Handle horizontal collisions"""
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.velocity.x > 0:
                    self.rect.right = tile.rect.left
                    self.facing_right = False
                elif self.velocity.x < 0:
                    self.rect.left = tile.rect.right
                    self.facing_right = True
                self.pos.x = self.rect.x
                self.velocity.x = 0
    
    def handle_collision_y(self, tiles):
        """Handle vertical collisions"""
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.velocity.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = tile.rect.bottom
                self.pos.y = self.rect.y
                self.velocity.y = 0
    
    def get_drops(self):
        """Get items to drop on death"""
        return self.drops
    
    def draw(self, surface, camera, assets):
        """Draw enemy"""
        screen_pos = camera.apply(self.rect)
        
        # Get sprite
        sprite = assets.get_image('enemies', self.enemy_type)
        
        # Flip if facing left
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        # Flash when hit
        if self.hit_timer.is_active():
            sprite = sprite.copy()
            sprite.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_ADD)
        
        surface.blit(sprite, screen_pos)
        
        # Draw health bar
        if self.hp < self.max_hp:
            bar_width = 40
            bar_height = 4
            bar_x = screen_pos.centerx - bar_width // 2
            bar_y = screen_pos.top - 10
            
            # Background
            pygame.draw.rect(surface, DARK_RED, 
                           (bar_x, bar_y, bar_width, bar_height))
            # Health
            health_width = int((self.hp / self.max_hp) * bar_width)
            pygame.draw.rect(surface, RED, 
                           (bar_x, bar_y, health_width, bar_height))
