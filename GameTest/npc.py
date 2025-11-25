"""
NPC system for dialogue and interactions
"""
import pygame
from config import *
from utils import Vector2

class NPC:
    def __init__(self, x, y, npc_type='villager', name='Villager', dialogue_key='default'):
        self.pos = Vector2(x, y)
        self.npc_type = npc_type
        self.name = name
        self.dialogue_key = dialogue_key
        self.rect = pygame.Rect(x, y, 48, 64)
        
        # Interaction
        self.interaction_range = 80
        self.can_interact = True
        self.is_merchant = npc_type == 'merchant'
        self.is_quest_giver = False
        
        # Quests
        self.active_quest = None
        self.quest_completed = False
        
        # Animation
        self.animation_frame = 0
        self.animation_timer = 0
        
        # Facing direction
        self.facing_right = True
    
    def update(self, dt, player):
        """Update NPC"""
        # Simple idle animation
        self.animation_timer += dt
        if self.animation_timer >= 500:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 2
        
        # Face player if nearby
        distance = abs(player.rect.centerx - self.rect.centerx)
        if distance < self.interaction_range:
            self.facing_right = player.rect.centerx > self.rect.centerx
    
    def can_interact_with(self, player):
        """Check if player can interact with NPC"""
        if not self.can_interact:
            return False
        
        distance = ((player.rect.centerx - self.rect.centerx) ** 2 + 
                   (player.rect.centery - self.rect.centery) ** 2) ** 0.5
        
        return distance < self.interaction_range
    
    def interact(self, player, story_manager):
        """Handle interaction with player"""
        if self.can_interact_with(player):
            # Return dialogue key for dialogue system
            if self.is_quest_giver and not self.quest_completed:
                return f"{self.dialogue_key}_quest"
            else:
                return self.dialogue_key
        return None
    
    def give_quest(self, quest_id):
        """Give a quest to player"""
        self.active_quest = quest_id
        self.is_quest_giver = True
    
    def complete_quest(self):
        """Mark quest as completed"""
        self.quest_completed = True
        self.is_quest_giver = False
    
    def draw(self, surface, camera, assets):
        """Draw NPC"""
        screen_pos = camera.apply(self.rect)
        
        # Get sprite
        sprite = assets.get_image('npcs', self.npc_type)
        
        # Flip if facing left
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        surface.blit(sprite, screen_pos)
        
        # Draw name above NPC
        font = assets.get_font('small')
        name_surface = font.render(self.name, True, WHITE)
        name_rect = name_surface.get_rect(centerx=screen_pos.centerx, 
                                         bottom=screen_pos.top - 5)
        
        # Name background
        bg_rect = name_rect.inflate(10, 4)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((*BLACK, 150))
        surface.blit(bg_surface, bg_rect)
        surface.blit(name_surface, name_rect)
        
        # Quest indicator
        if self.is_quest_giver and not self.quest_completed:
            # Yellow exclamation mark
            indicator_pos = (screen_pos.centerx, screen_pos.top - 25)
            pygame.draw.circle(surface, YELLOW, indicator_pos, 8)
            font_small = assets.get_font('small')
            exclaim = font_small.render("!", True, BLACK)
            exclaim_rect = exclaim.get_rect(center=indicator_pos)
            surface.blit(exclaim, exclaim_rect)

class NPCManager:
    def __init__(self):
        self.npcs = []
    
    def add_npc(self, npc):
        """Add NPC to manager"""
        self.npcs.append(npc)
        return npc
    
    def create_npc(self, x, y, npc_type, name, dialogue_key):
        """Create and add NPC"""
        npc = NPC(x, y, npc_type, name, dialogue_key)
        self.npcs.append(npc)
        return npc
    
    def update(self, dt, player):
        """Update all NPCs"""
        for npc in self.npcs:
            npc.update(dt, player)
    
    def get_interactable_npc(self, player):
        """Get NPC that player can currently interact with"""
        for npc in self.npcs:
            if npc.can_interact_with(player):
                return npc
        return None
    
    def draw(self, surface, camera, assets):
        """Draw all NPCs"""
        for npc in self.npcs:
            npc.draw(surface, camera, assets)
    
    def get_npc_by_name(self, name):
        """Get NPC by name"""
        for npc in self.npcs:
            if npc.name == name:
                return npc
        return None
