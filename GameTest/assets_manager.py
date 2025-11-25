"""
Asset Manager - Handles loading and caching of game assets
"""
import pygame
import os
from utils import create_placeholder_surface, load_image
from config import *

class AssetManager:
    def __init__(self):
        self.images = {}
        self.fonts = {}
        self.sounds = {}
        self.spritesheets = {}
        
        # Initialize pygame font
        pygame.font.init()
        
        # Load default font
        self.fonts['default'] = pygame.font.Font(None, 24)
        self.fonts['small'] = pygame.font.Font(None, 18)
        self.fonts['medium'] = pygame.font.Font(None, 32)
        self.fonts['large'] = pygame.font.Font(None, 48)
        self.fonts['title'] = pygame.font.Font(None, 72)
    
    def load_player_sprites(self):
        """Load or create player sprites"""
        # Create placeholder player sprites
        player_sprites = {
            'idle': self._create_player_sprite(BLUE, 'idle'),
            'walk': [self._create_player_sprite(BLUE, f'walk{i}') for i in range(6)],
            'jump': self._create_player_sprite(BLUE, 'jump'),
            'fall': self._create_player_sprite(BLUE, 'fall'),
            'attack': [self._create_player_sprite(PURPLE, f'attack{i}') for i in range(4)],
            'cast': [self._create_player_sprite(CYAN, f'cast{i}') for i in range(4)],
            'hit': self._create_player_sprite(RED, 'hit'),
            'dead': self._create_player_sprite(DARK_GRAY, 'dead')
        }
        self.images['player'] = player_sprites
        return player_sprites
    
    def _create_player_sprite(self, color, label):
        """Create a placeholder player sprite"""
        surf = pygame.Surface((48, 64), pygame.SRCALPHA)
        # Body
        pygame.draw.rect(surf, color, (12, 16, 24, 32))
        # Head
        pygame.draw.circle(surf, color, (24, 12), 10)
        # Staff (for non-dead states)
        if label != 'dead':
            pygame.draw.line(surf, (139, 69, 19), (36, 20), (36, 50), 3)
            pygame.draw.circle(surf, PURPLE, (36, 16), 4)
        return surf
    
    def load_enemy_sprites(self):
        """Load or create enemy sprites"""
        enemies = {
            'slime': self._create_enemy_sprite(GREEN, 32, 24, 'slime'),
            'skeleton': self._create_enemy_sprite(LIGHT_GRAY, 48, 64, 'skeleton'),
            'shadow_beast': self._create_enemy_sprite(DARK_GRAY, 64, 48, 'beast'),
            'corrupted_mage': self._create_enemy_sprite(PURPLE, 48, 64, 'mage'),
            'bat': self._create_enemy_sprite((80, 60, 40), 32, 24, 'bat'),
        }
        self.images['enemies'] = enemies
        return enemies
    
    def _create_enemy_sprite(self, color, width, height, enemy_type):
        """Create placeholder enemy sprite"""
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        if enemy_type == 'slime':
            pygame.draw.ellipse(surf, color, (0, height//2, width, height//2))
            pygame.draw.circle(surf, BLACK, (width//3, height//2), 4)
            pygame.draw.circle(surf, BLACK, (2*width//3, height//2), 4)
        elif enemy_type == 'skeleton':
            pygame.draw.rect(surf, color, (width//4, height//2, width//2, height//2))
            pygame.draw.circle(surf, color, (width//2, height//4), height//4)
        elif enemy_type == 'beast':
            pygame.draw.ellipse(surf, color, (0, 0, width, height))
            pygame.draw.circle(surf, RED, (width//3, height//3), 4)
            pygame.draw.circle(surf, RED, (2*width//3, height//3), 4)
        elif enemy_type == 'mage':
            pygame.draw.rect(surf, color, (width//4, height//3, width//2, 2*height//3))
            pygame.draw.circle(surf, color, (width//2, height//6), height//6)
        elif enemy_type == 'bat':
            pygame.draw.ellipse(surf, color, (width//4, 0, width//2, height//2))
            pygame.draw.polygon(surf, color, [(0, height//2), (width//3, height//4), (width//3, height)])
            pygame.draw.polygon(surf, color, [(width, height//2), (2*width//3, height//4), (2*width//3, height)])
        return surf
    
    def load_boss_sprites(self):
        """Load or create boss sprites"""
        bosses = {
            'forest_guardian': self._create_boss_sprite((101, 67, 33), 128, 128, 'tree'),
            'crystal_golem': self._create_boss_sprite(CYAN, 96, 128, 'golem'),
            'shadow_lord': self._create_boss_sprite((20, 0, 40), 128, 128, 'lord')
        }
        self.images['bosses'] = bosses
        return bosses
    
    def _create_boss_sprite(self, color, width, height, boss_type):
        """Create placeholder boss sprite"""
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        if boss_type == 'tree':
            # Trunk
            pygame.draw.rect(surf, color, (width//3, height//2, width//3, height//2))
            # Canopy
            pygame.draw.circle(surf, GREEN, (width//2, height//3), width//3)
        elif boss_type == 'golem':
            pygame.draw.rect(surf, color, (width//4, height//3, width//2, 2*height//3))
            pygame.draw.rect(surf, color, (width//3, height//6, width//3, height//4))
        elif boss_type == 'lord':
            pygame.draw.rect(surf, color, (width//4, height//3, width//2, 2*height//3))
            pygame.draw.circle(surf, color, (width//2, height//6), height//6)
            # Shadow aura
            surf_aura = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.circle(surf_aura, (*color, 100), (width//2, height//2), width//2)
            surf.blit(surf_aura, (0, 0))
        return surf
    
    def load_npc_sprites(self):
        """Load or create NPC sprites"""
        npcs = {
            'elder': self._create_npc_sprite(LIGHT_GRAY, 'elder'),
            'merchant': self._create_npc_sprite(ORANGE, 'merchant'),
            'villager': self._create_npc_sprite(GREEN, 'villager'),
            'blacksmith': self._create_npc_sprite((139, 69, 19), 'blacksmith'),
            'mage': self._create_npc_sprite(PURPLE, 'mage'),
        }
        self.images['npcs'] = npcs
        return npcs
    
    def _create_npc_sprite(self, color, npc_type):
        """Create placeholder NPC sprite"""
        surf = pygame.Surface((48, 64), pygame.SRCALPHA)
        # Body
        pygame.draw.rect(surf, color, (12, 24, 24, 32))
        # Head
        pygame.draw.circle(surf, color, (24, 16), 10)
        # Accessories based on type
        if npc_type == 'elder':
            pygame.draw.line(surf, WHITE, (24, 26), (30, 40), 2)  # Staff
        elif npc_type == 'merchant':
            pygame.draw.rect(surf, (101, 67, 33), (10, 30, 28, 10))  # Bag
        return surf
    
    def load_tile_sprites(self):
        """Load or create tile sprites"""
        tiles = {
            'grass': self._create_tile_sprite(GREEN, 'grass'),
            'dirt': self._create_tile_sprite((139, 69, 19), 'dirt'),
            'stone': self._create_tile_sprite(GRAY, 'stone'),
            'wood': self._create_tile_sprite((101, 67, 33), 'wood'),
            'crystal': self._create_tile_sprite(CYAN, 'crystal'),
            'shadow': self._create_tile_sprite((40, 0, 60), 'shadow'),
        }
        self.images['tiles'] = tiles
        return tiles
    
    def _create_tile_sprite(self, color, tile_type):
        """Create placeholder tile sprite"""
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surf.fill(color)
        # Add texture pattern
        darker = tuple(max(0, c - 30) for c in color[:3])
        for i in range(0, TILE_SIZE, 8):
            pygame.draw.line(surf, darker, (i, 0), (i, TILE_SIZE), 1)
            pygame.draw.line(surf, darker, (0, i), (TILE_SIZE, i), 1)
        return surf
    
    def load_ui_sprites(self):
        """Load or create UI sprites"""
        ui = {
            'heart_full': self._create_heart(RED, True),
            'heart_empty': self._create_heart(DARK_RED, False),
            'mana_orb': self._create_orb(BLUE),
            'dialogue_box': self._create_dialogue_box(),
        }
        self.images['ui'] = ui
        return ui
    
    def _create_heart(self, color, filled):
        """Create heart sprite for HP"""
        surf = pygame.Surface((16, 16), pygame.SRCALPHA)
        if filled:
            pygame.draw.circle(surf, color, (5, 6), 5)
            pygame.draw.circle(surf, color, (11, 6), 5)
            pygame.draw.polygon(surf, color, [(0, 7), (8, 15), (16, 7)])
        else:
            pygame.draw.circle(surf, color, (5, 6), 5, 1)
            pygame.draw.circle(surf, color, (11, 6), 5, 1)
            pygame.draw.lines(surf, color, False, [(0, 7), (8, 15), (16, 7)], 1)
        return surf
    
    def _create_orb(self, color):
        """Create orb sprite for mana"""
        surf = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (6, 6), 6)
        pygame.draw.circle(surf, WHITE, (4, 4), 2)
        return surf
    
    def _create_dialogue_box(self):
        """Create dialogue box background"""
        surf = pygame.Surface((SCREEN_WIDTH - 100, 180), pygame.SRCALPHA)
        pygame.draw.rect(surf, UI_BG_COLOR, (0, 0, surf.get_width(), surf.get_height()))
        pygame.draw.rect(surf, UI_BORDER_COLOR, (0, 0, surf.get_width(), surf.get_height()), 3)
        return surf
    
    def load_magic_sprites(self):
        """Load or create magic effect sprites"""
        magic = {
            ELEMENT_FIRE: self._create_magic_projectile(ORANGE),
            ELEMENT_ICE: self._create_magic_projectile(CYAN),
            ELEMENT_LIGHTNING: self._create_magic_projectile(YELLOW),
            ELEMENT_EARTH: self._create_magic_projectile((139, 69, 19)),
            ELEMENT_WIND: self._create_magic_projectile(LIGHT_GRAY),
        }
        self.images['magic'] = magic
        return magic
    
    def _create_magic_projectile(self, color):
        """Create magic projectile sprite"""
        surf = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (12, 12), 10)
        pygame.draw.circle(surf, WHITE, (12, 12), 5)
        return surf
    
    def load_all_assets(self):
        """Load all game assets"""
        print("Loading game assets...")
        self.load_player_sprites()
        self.load_enemy_sprites()
        self.load_boss_sprites()
        self.load_npc_sprites()
        self.load_tile_sprites()
        self.load_ui_sprites()
        self.load_magic_sprites()
        print("Assets loaded successfully!")
    
    def get_image(self, category, name):
        """Get an image from the asset manager"""
        if category in self.images and name in self.images[category]:
            return self.images[category][name]
        return create_placeholder_surface(32, 32)
    
    def get_font(self, name='default'):
        """Get a font"""
        return self.fonts.get(name, self.fonts['default'])

# Global asset manager instance
assets = AssetManager()
