"""
UI Manager - HUD, menus, and UI elements
"""
import pygame
from config import *
from utils import draw_text
import random

class UI_Manager:
    def __init__(self):
        self.show_fps = False
        self.notification_text = ""
        self.notification_timer = 0
        self.notification_duration = 2000
        
    def draw_hud(self, surface, player, assets):
        """Draw player HUD"""
        font = assets.get_font('default')
        small_font = assets.get_font('small')
        
        # HP Bar
        hp_bar_x = 20
        hp_bar_y = 20
        hp_bar_width = 200
        hp_bar_height = 25
        
        # HP Background
        pygame.draw.rect(surface, BLACK, 
                        (hp_bar_x - 2, hp_bar_y - 2, hp_bar_width + 4, hp_bar_height + 4))
        pygame.draw.rect(surface, DARK_RED, 
                        (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))
        
        # HP Fill
        hp_ratio = player.hp / player.max_hp
        hp_fill_width = int(hp_bar_width * hp_ratio)
        pygame.draw.rect(surface, HP_BAR_COLOR, 
                        (hp_bar_x, hp_bar_y, hp_fill_width, hp_bar_height))
        
        # HP Text
        hp_text = f"HP: {int(player.hp)}/{player.max_hp}"
        text_surf = small_font.render(hp_text, True, WHITE)
        surface.blit(text_surf, (hp_bar_x + 5, hp_bar_y + 5))
        
        # MP Bar
        mp_bar_x = 20
        mp_bar_y = 50
        mp_bar_width = 200
        mp_bar_height = 20
        
        # MP Background
        pygame.draw.rect(surface, BLACK, 
                        (mp_bar_x - 2, mp_bar_y - 2, mp_bar_width + 4, mp_bar_height + 4))
        pygame.draw.rect(surface, DARK_BLUE, 
                        (mp_bar_x, mp_bar_y, mp_bar_width, mp_bar_height))
        
        # MP Fill
        mp_ratio = player.mp / player.max_mp
        mp_fill_width = int(mp_bar_width * mp_ratio)
        pygame.draw.rect(surface, MP_BAR_COLOR, 
                        (mp_bar_x, mp_bar_y, mp_fill_width, mp_bar_height))
        
        # MP Text
        mp_text = f"MP: {int(player.mp)}/{player.max_mp}"
        text_surf = small_font.render(mp_text, True, WHITE)
        surface.blit(text_surf, (mp_bar_x + 5, mp_bar_y + 2))
        
        # XP Bar
        xp_bar_x = 20
        xp_bar_y = 75
        xp_bar_width = 200
        xp_bar_height = 15
        
        # XP Background
        pygame.draw.rect(surface, BLACK, 
                        (xp_bar_x - 2, xp_bar_y - 2, xp_bar_width + 4, xp_bar_height + 4))
        pygame.draw.rect(surface, DARK_GRAY, 
                        (xp_bar_x, xp_bar_y, xp_bar_width, xp_bar_height))
        
        # XP Fill
        xp_ratio = player.experience / player.experience_to_next_level
        xp_fill_width = int(xp_bar_width * xp_ratio)
        pygame.draw.rect(surface, XP_BAR_COLOR, 
                        (xp_bar_x, xp_bar_y, xp_fill_width, xp_bar_height))
        
        # Level text
        level_text = f"Level {player.level}"
        text_surf = font.render(level_text, True, YELLOW)
        surface.blit(text_surf, (20, 95))
        
        # Gold
        gold_text = f"Gold: {player.gold}"
        text_surf = font.render(gold_text, True, YELLOW)
        surface.blit(text_surf, (20, 120))
        
        # Selected spell indicator
        spell_x = SCREEN_WIDTH - 250
        spell_y = 20
        
        spell_names = {
            ELEMENT_FIRE: "Fire Bolt",
            ELEMENT_ICE: "Ice Shard",
            ELEMENT_LIGHTNING: "Lightning Strike",
            ELEMENT_EARTH: "Earth Spike",
            ELEMENT_WIND: "Wind Gust"
        }
        
        selected_spell_text = f"Spell: {spell_names.get(player.selected_spell, 'None')}"
        text_surf = font.render(selected_spell_text, True, WHITE)
        surface.blit(text_surf, (spell_x, spell_y))
        
        # Spell icons
        spell_icon_y = spell_y + 30
        for i, element in enumerate([ELEMENT_FIRE, ELEMENT_ICE, ELEMENT_LIGHTNING, 
                                     ELEMENT_EARTH, ELEMENT_WIND]):
            if element in player.unlocked_spells:
                icon_x = spell_x + i * 35
                
                # Icon background
                if element == player.selected_spell:
                    pygame.draw.rect(surface, YELLOW, 
                                   (icon_x - 2, spell_icon_y - 2, 34, 34))
                
                pygame.draw.rect(surface, DARK_GRAY, 
                               (icon_x, spell_icon_y, 30, 30))
                
                # Element color
                colors = {
                    ELEMENT_FIRE: ORANGE,
                    ELEMENT_ICE: CYAN,
                    ELEMENT_LIGHTNING: YELLOW,
                    ELEMENT_EARTH: (139, 69, 19),
                    ELEMENT_WIND: LIGHT_GRAY
                }
                
                pygame.draw.circle(surface, colors[element], 
                                 (icon_x + 15, spell_icon_y + 15), 12)
                
                # Number
                num_surf = small_font.render(str(i + 1), True, BLACK)
                surface.blit(num_surf, (icon_x + 12, spell_icon_y + 10))
        
        # Controls help
        help_y = SCREEN_HEIGHT - 100
        help_texts = [
            "WASD/Arrows: Move",
            "Space: Jump",
            "J/Z: Attack",
            "K/X: Cast Spell",
            "1-5: Select Spell",
            "E: Interact"
        ]
        
        for i, text in enumerate(help_texts):
            text_surf = small_font.render(text, True, LIGHT_GRAY)
            surface.blit(text_surf, (20, help_y + i * 15))
        
        # Notification
        if self.notification_timer > 0:
            notif_font = assets.get_font('medium')
            notif_surf = notif_font.render(self.notification_text, True, YELLOW)
            notif_rect = notif_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
            
            # Background
            bg_rect = notif_rect.inflate(20, 10)
            bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surf.fill((*BLACK, 180))
            surface.blit(bg_surf, bg_rect)
            
            surface.blit(notif_surf, notif_rect)
    
    def show_notification(self, text, duration=2000):
        """Show a notification message"""
        self.notification_text = text
        self.notification_timer = duration
        self.notification_duration = duration
    
    def update(self, dt):
        """Update UI elements"""
        if self.notification_timer > 0:
            self.notification_timer -= dt
    
    def draw_main_menu(self, surface, assets):
        """Draw main menu"""
        # Background
        surface.fill((20, 20, 40))
        
        # Title
        title_font = assets.get_font('title')
        title_text = "Chronicles of Aethermoor"
        title_surf = title_font.render(title_text, True, YELLOW)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        
        # Title shadow
        shadow_surf = title_font.render(title_text, True, BLACK)
        surface.blit(shadow_surf, (title_rect.x + 3, title_rect.y + 3))
        surface.blit(title_surf, title_rect)
        
        # Subtitle
        medium_font = assets.get_font('medium')
        subtitle = "An Elemental Adventure"
        subtitle_surf = medium_font.render(subtitle, True, CYAN)
        subtitle_rect = subtitle_surf.get_rect(center=(SCREEN_WIDTH // 2, 220))
        surface.blit(subtitle_surf, subtitle_rect)
        
        # Menu options
        menu_y = 350
        menu_options = ["Start New Game", "Continue (Not Yet Implemented)", "Quit"]
        
        for i, option in enumerate(menu_options):
            text_surf = medium_font.render(option, True, WHITE if i != 1 else GRAY)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, menu_y + i * 70))
            surface.blit(text_surf, text_rect)
        
        # Instructions
        small_font = assets.get_font('small')
        instructions = [
            "Use mouse to click options",
            "or press ENTER to start"
        ]
        
        for i, text in enumerate(instructions):
            text_surf = small_font.render(text, True, LIGHT_GRAY)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80 + i * 20))
            surface.blit(text_surf, text_rect)
    
    def draw_pause_menu(self, surface, assets):
        """Draw pause menu"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*BLACK, 150))
        surface.blit(overlay, (0, 0))
        
        # Pause text
        large_font = assets.get_font('large')
        pause_text = "PAUSED"
        pause_surf = large_font.render(pause_text, True, YELLOW)
        pause_rect = pause_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        surface.blit(pause_surf, pause_rect)
        
        # Options
        medium_font = assets.get_font('medium')
        options = ["Resume", "Restart Level", "Main Menu", "Quit"]
        
        for i, option in enumerate(options):
            text_surf = medium_font.render(option, True, WHITE)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, 
                                                   SCREEN_HEIGHT // 2 + i * 50))
            surface.blit(text_surf, text_rect)
    
    def draw_game_over(self, surface, assets):
        """Draw game over screen"""
        # Background
        surface.fill((20, 0, 0))
        
        # Game Over text
        large_font = assets.get_font('large')
        text = "GAME OVER"
        text_surf = large_font.render(text, True, RED)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(text_surf, text_rect)
        
        # Continue text
        small_font = assets.get_font('small')
        continue_text = "Press ENTER to return to menu"
        continue_surf = small_font.render(continue_text, True, WHITE)
        continue_rect = continue_surf.get_rect(center=(SCREEN_WIDTH // 2, 
                                                       SCREEN_HEIGHT // 2 + 80))
        surface.blit(continue_surf, continue_rect)
