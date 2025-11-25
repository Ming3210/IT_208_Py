"""
Tile system for level building
"""
import pygame
from config import *

class Tile:
    def __init__(self, x, y, tile_type='grass', solid=True):
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.tile_type = tile_type
        self.solid = solid
        self.animated = False
        self.damage = 0
        
        # Tile properties
        if tile_type == 'spike':
            self.damage = 10
        elif tile_type == 'lava':
            self.damage = 20
            self.animated = True
    
    def draw(self, surface, camera, assets):
        """Draw tile"""
        if not camera.is_visible(self.rect):
            return
        
        screen_pos = camera.apply(self.rect)
        
        # Get tile sprite
        tile_sprite = assets.get_image('tiles', self.tile_type)
        surface.blit(tile_sprite, screen_pos)

class TileMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []
        self.solid_tiles = []
    
    def add_tile(self, x, y, tile_type='grass', solid=True):
        """Add a tile to the map"""
        tile = Tile(x, y, tile_type, solid)
        self.tiles.append(tile)
        if solid:
            self.solid_tiles.append(tile)
        return tile
    
    def get_tile_at(self, x, y):
        """Get tile at grid position"""
        for tile in self.tiles:
            grid_x = tile.rect.x // TILE_SIZE
            grid_y = tile.rect.y // TILE_SIZE
            if grid_x == x and grid_y == y:
                return tile
        return None
    
    def remove_tile(self, x, y):
        """Remove tile at grid position"""
        tile = self.get_tile_at(x, y)
        if tile:
            self.tiles.remove(tile)
            if tile in self.solid_tiles:
                self.solid_tiles.remove(tile)
    
    def get_nearby_tiles(self, rect, radius=2):
        """Get tiles near a rect"""
        nearby = []
        for tile in self.solid_tiles:
            if abs(tile.rect.centerx - rect.centerx) < radius * TILE_SIZE * 3:
                if abs(tile.rect.centery - rect.centery) < radius * TILE_SIZE * 3:
                    nearby.append(tile)
        return nearby
    
    def draw(self, surface, camera, assets):
        """Draw all tiles"""
        for tile in self.tiles:
            tile.draw(surface, camera, assets)
    
    def create_platform(self, start_x, start_y, length, tile_type='grass'):
        """Create a horizontal platform"""
        for i in range(length):
            self.add_tile(start_x + i, start_y, tile_type, True)
    
    def create_wall(self, start_x, start_y, height, tile_type='stone'):
        """Create a vertical wall"""
        for i in range(height):
            self.add_tile(start_x, start_y + i, tile_type, True)
    
    def create_room(self, start_x, start_y, width, height, tile_type='stone'):
        """Create a rectangular room"""
        # Floor
        for x in range(width):
            self.add_tile(start_x + x, start_y + height - 1, tile_type, True)
        
        # Ceiling
        for x in range(width):
            self.add_tile(start_x + x, start_y, tile_type, True)
        
        # Walls
        for y in range(1, height - 1):
            self.add_tile(start_x, start_y + y, tile_type, True)
            self.add_tile(start_x + width - 1, start_y + y, tile_type, True)
