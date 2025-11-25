"""
Level system
"""
import pygame
from tiles import TileMap
from enemy import Enemy
from boss import Boss
from npc import NPC
from config import *

class Level:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.tilemap = TileMap(width, height)
        self.enemies = []
        self.bosses = []
        self.npcs = []
        self.spawn_point = (100, 100)
        self.exit_portal = None  # Exit portal rect
        self.completed = False
        
    def add_enemy(self, x, y, enemy_type):
        """Add enemy to level"""
        enemy = Enemy(x, y, enemy_type)
        self.enemies.append(enemy)
        return enemy
    
    def add_boss(self, x, y, boss_type):
        """Add boss to level"""
        boss = Boss(x, y, boss_type)
        self.bosses.append(boss)
        return boss
    
    def add_npc(self, x, y, npc_type, name, dialogue_key):
        """Add NPC to level"""
        npc = NPC(x, y, npc_type, name, dialogue_key)
        self.npcs.append(npc)
        return npc
    
    def update(self, dt, player):
        """Update level entities"""
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(dt, player, self.tilemap.solid_tiles)
            
            # Check if enemy is dead
            if enemy.hp <= 0:
                self.enemies.remove(enemy)
                # Drop items/gold
                player.gold += enemy.get_drops()[0][1]  # Get gold
                player.gain_experience(enemy.xp_value)
        
        # Update bosses
        for boss in self.bosses[:]:
            boss.update(dt, player, self.tilemap.solid_tiles)
            
            if boss.hp <= 0:
                self.bosses.remove(boss)
                player.gain_experience(boss.xp_value)
                self.completed = True
        
        # Update NPCs
        for npc in self.npcs:
            npc.update(dt, player)
        
        # Check exit portal collision
        if self.exit_portal and player.rect.colliderect(self.exit_portal):
            self.completed = True
    
    def draw(self, surface, camera, assets):
        """Draw level"""
        # Draw tiles
        self.tilemap.draw(surface, camera, assets)
        
        # Draw NPCs
        for npc in self.npcs:
            npc.draw(surface, camera, assets)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(surface, camera, assets)
        
        # Draw bosses
        for boss in self.bosses:
            boss.draw(surface, camera, assets)
        
        # Draw exit portal
        if self.exit_portal:
            screen_pos = camera.apply(self.exit_portal)
            # Pulsing portal effect
            pulse = abs((pygame.time.get_ticks() % 2000) - 1000) / 1000.0
            color = (100 + int(155 * pulse), 100 + int(155 * pulse), 255)
            pygame.draw.rect(surface, color, screen_pos, 0)
            pygame.draw.rect(surface, (255, 255, 255), screen_pos, 3)

def create_village_level():
    """Create the starting village level"""
    level = Level("Heartwood Village", 100, 30)
    
    # Ground
    level.tilemap.create_platform(0, 25, 100, 'grass')
    
    # Buildings and platforms for more interesting traversal
    level.tilemap.create_platform(10, 20, 8, 'wood')
    level.tilemap.create_platform(25, 20, 10, 'wood')
    level.tilemap.create_platform(45, 20, 8, 'wood')
    level.tilemap.create_platform(60, 20, 10, 'wood')
    level.tilemap.create_platform(75, 20, 8, 'wood')
    level.tilemap.create_platform(90, 20, 8, 'wood')
    
    # NPCs
    level.add_npc(300, 640, 'elder', 'Elder Theron', 'elder_intro')
    level.add_npc(800, 640, 'merchant', 'Merchant Gris', 'merchant')
    level.add_npc(1600, 640, 'blacksmith', 'Blacksmith Bram', 'blacksmith')
    level.add_npc(500, 640, 'villager', 'Villager', 'villager1')
    level.add_npc(1200, 640, 'villager', 'Old Woman', 'villager2')
    
    level.spawn_point = (100, 600)
    level.exit_portal = pygame.Rect(3000, 550, 64, 100)  # Exit to forest
    
    return level

def create_forest_level():
    """Create the forest level"""
    level = Level("Whispering Woods", 150, 30)
    
    # Ground with variations
    level.tilemap.create_platform(0, 25, 150, 'grass')
    
    # Platforms - wider spacing for easier jumping
    # Need enough platforms to reach exit at x=4500
    for i in range(15):  # Increased to 15 platforms
        x = 10 + i * 16  # 16 tiles spacing
        y = 20 - (i % 3) * 3
        level.tilemap.create_platform(x, y, 5, 'wood')
    
    # Enemies
    level.add_enemy(800, 640, 'slime')
    level.add_enemy(1200, 640, 'slime')
    level.add_enemy(1600, 640, 'bat')
    level.add_enemy(2000, 640, 'skeleton')
    level.add_enemy(2400, 640, 'slime')
    level.add_enemy(2800, 640, 'skeleton')
    level.add_enemy(3200, 640, 'bat')  # Additional enemy
    level.add_enemy(3600, 640, 'skeleton')  # Additional enemy
    
    level.spawn_point = (100, 600)
    level.exit_portal = pygame.Rect(4200, 550, 64, 100)  # Moved closer from 4500
    
    return level

def create_wind_shrine_level():
    """Create the Wind Shrine level"""
    level = Level("Shrine of Winds", 120, 30)
    
    # Complex platforming
    level.tilemap.create_platform(0, 25, 20, 'stone')
    
    # Vertical challenge
    for i in range(8):
        x = 25 + (i % 2) * 10
        y = 24 - i * 2
        level.tilemap.create_platform(x, y, 4, 'stone')
    
    # Platforms to boss area - continuous path
    for i in range(12):
        x = 50 + i * 12
        y = 25 - (i % 4) * 2
        level.tilemap.create_platform(x, y, 6, 'stone')
    
    # Enemies
    level.add_enemy(1000, 640, 'bat')
    level.add_enemy(1400, 400, 'bat')
    level.add_enemy(1800, 200, 'bat')
    level.add_enemy(2400, 640, 'shadow_beast')
    
    # Boss - Forest Guardian
    level.add_boss(3200, 640, 'forest_guardian')
    
    level.spawn_point = (100, 600)
    # Exit portal appears after boss is defeated (handled in main.py)
    
    return level

def create_cave_level():
    """Create the Crystal Caves level"""
    level = Level("Crystal Caves", 130, 30)
    
    # Cave floor
    level.tilemap.create_platform(0, 25, 130, 'stone')
    
    # Ceiling hazards
    level.tilemap.create_platform(0, 5, 130, 'stone')
    
    # Platforms
    for i in range(12):
        x = 10 + i * 9
        y = 20 - (i % 4) * 2
        level.tilemap.create_platform(x, y, 4, 'crystal')
    
    # Enemies
    level.add_enemy(600, 640, 'slime')
    level.add_enemy(1000, 640, 'skeleton')
    level.add_enemy(1400, 640, 'corrupted_mage')
    level.add_enemy(1800, 640, 'skeleton')
    level.add_enemy(2200, 640, 'shadow_beast')
    level.add_enemy(2600, 640, 'corrupted_mage')
    
    # Boss - Crystal Golem
    level.add_boss(3600, 640, 'crystal_golem')
    
    level.spawn_point = (100, 600)
    # Exit portal appears after boss is defeated (handled in main.py)
    
    return level

def create_shadow_citadel_level():
    """Create the final Shadow Citadel level"""
    level = Level("Shadow Citadel", 100, 30)
    
    # Dark stone floor
    level.tilemap.create_platform(0, 25, 100, 'shadow')
    
    # Platforms leading to boss
    for i in range(8):
        x = 10 + i * 10
        y = 23 - (i % 2) * 2
        level.tilemap.create_platform(x, y, 5, 'shadow')
    
    # Elite enemies
    level.add_enemy(1000, 640, 'shadow_beast')
    level.add_enemy(1400, 640, 'corrupted_mage')
    level.add_enemy(1800, 640, 'shadow_beast')
    level.add_enemy(2200, 640, 'corrupted_mage')
    
    # Final Boss - Shadow Lord
    level.add_boss(2800, 640, 'shadow_lord')
    
    level.spawn_point = (100, 600)
    # No exit portal - final level
    
    return level

# Level progression
LEVELS = {
    'village': create_village_level,
    'forest': create_forest_level,
    'wind_shrine': create_wind_shrine_level,
    'caves': create_cave_level,
    'citadel': create_shadow_citadel_level
}

LEVEL_ORDER = ['village', 'forest', 'wind_shrine', 'caves', 'citadel']
