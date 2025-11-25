"""
Dialogue system with typewriter effect and choices
"""
import pygame
from config import *
from utils import Timer

class DialogueBox:
    def __init__(self):
        self.active = False
        self.current_text = ""
        self.full_text = ""
        self.character_index = 0
        self.text_speed = 50  # ms per character
        self.timer = 0
        
        # Speaker
        self.speaker_name = ""
        self.portrait = None
        
        # Choices
        self.choices = []
        self.selected_choice = 0
        self.waiting_for_choice = False
        
        # Callback
        self.on_complete = None
        self.choice_callback = None
    
    def start_dialogue(self, text, speaker="", choices=None, callback=None):
        """Start displaying dialogue"""
        self.active = True
        self.full_text = text
        self.current_text = ""
        self.character_index = 0
        self.speaker_name = speaker
        self.timer = 0
        
        if choices:
            self.choices = choices
            self.selected_choice = 0
            self.waiting_for_choice = False
        else:
            self.choices = []
            self.waiting_for_choice = False
        
        self.on_complete = callback
    
    def update(self, dt, events):
        """Update dialogue display"""
        if not self.active:
            return None
        
        # If waiting for choice, handle choice input
        if self.waiting_for_choice:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        self.selected_choice = (self.selected_choice - 1) % len(self.choices)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.selected_choice = (self.selected_choice + 1) % len(self.choices)
                    elif event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_z]:
                        # Choice selected
                        choice = self.choices[self.selected_choice]
                        self.active = False
                        return ('choice', choice)
            return None
        
        # Typewriter effect
        if self.character_index < len(self.full_text):
            # Allow skipping typewriter effect
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_z]:
                        self.skip_typewriter()
                        return None
            
            self.timer += dt
            while self.timer >= self.text_speed and self.character_index < len(self.full_text):
                self.current_text += self.full_text[self.character_index]
                self.character_index += 1
                self.timer -= self.text_speed
        else:
            # Text fully displayed
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_z]:
                        if self.choices:
                            # Show choices
                            self.waiting_for_choice = True
                        else:
                            # End dialogue
                            self.active = False
                            if self.on_complete:
                                self.on_complete()
                            return ('complete', None)
        
        return None
    
    def skip_typewriter(self):
        """Skip to full text"""
        self.current_text = self.full_text
        self.character_index = len(self.full_text)
    
    def draw(self, surface, assets):
        """Draw dialogue box"""
        if not self.active:
            return
        
        # Get dialogue box sprite
        box_sprite = assets.get_image('ui', 'dialogue_box')
        box_x = 50
        box_y = SCREEN_HEIGHT - 200
        
        surface.blit(box_sprite, (box_x, box_y))
        
        # Draw speaker name
        if self.speaker_name:
            font = assets.get_font('medium')
            name_surface = font.render(self.speaker_name, True, YELLOW)
            surface.blit(name_surface, (box_x + 20, box_y + 10))
        
        # Draw text
        font = assets.get_font('default')
        text_y = box_y + 50 if self.speaker_name else box_y + 20
        
        # Word wrap
        words = self.current_text.split(' ')
        lines = []
        current_line = ""
        max_width = SCREEN_WIDTH - 180
        
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word + " "
        
        if current_line:
            lines.append(current_line)
        
        # Draw lines
        for i, line in enumerate(lines[:4]):  # Max 4 lines
            line_surface = font.render(line, True, WHITE)
            surface.blit(line_surface, (box_x + 20, text_y + i * 30))
        
        # Draw choices if waiting
        if self.waiting_for_choice and self.choices:
            choice_y = box_y - len(self.choices) * 40 - 20
            
            for i, choice in enumerate(self.choices):
                # Background
                choice_rect = pygame.Rect(box_x + 20, choice_y + i * 40, 400, 35)
                color = UI_HIGHLIGHT_COLOR if i == self.selected_choice else UI_BG_COLOR
                pygame.draw.rect(surface, color, choice_rect)
                pygame.draw.rect(surface, UI_BORDER_COLOR, choice_rect, 2)
                
                # Text
                choice_surface = font.render(choice, True, BLACK if i == self.selected_choice else WHITE)
                surface.blit(choice_surface, (box_x + 30, choice_y + i * 40 + 8))
        
        # Continue indicator
        elif self.character_index >= len(self.full_text) and not self.choices:
            # Blinking arrow
            if (pygame.time.get_ticks() // 500) % 2:
                arrow_font = assets.get_font('medium')
                arrow = arrow_font.render("▼", True, WHITE)
                surface.blit(arrow, (SCREEN_WIDTH - 100, box_y + 140))

class DialogueManager:
    def __init__(self):
        self.dialogue_box = DialogueBox()
        self.dialogue_trees = {}
        self.current_tree = None
        self.current_node = 0
    
    def load_dialogue_tree(self, key, tree):
        """Load a dialogue tree"""
        self.dialogue_trees[key] = tree
    
    def start_dialogue(self, key):
        """Start a dialogue tree"""
        if key in self.dialogue_trees:
            self.current_tree = self.dialogue_trees[key]
            self.current_node = 0
            self.show_current_node()
            return True
        return False
    
    def show_current_node(self):
        """Show current dialogue node"""
        if not self.current_tree or self.current_node >= len(self.current_tree):
            return
        
        node = self.current_tree[self.current_node]
        
        text = node.get('text', '')
        speaker = node.get('speaker', '')
        choices = node.get('choices', None)
        
        self.dialogue_box.start_dialogue(text, speaker, choices)
    
    def update(self, dt, events):
        """Update dialogue system"""
        result = self.dialogue_box.update(dt, events)
        
        if result:
            event_type, data = result
            
            if event_type == 'complete':
                # Move to next node
                self.current_node += 1
                if self.current_node < len(self.current_tree):
                    self.show_current_node()
                else:
                    # Dialogue complete
                    self.current_tree = None
                    return ('complete', None)
            
            elif event_type == 'choice':
                # Handle choice
                return('choice', data)
        
        return None
    
    def is_active(self):
        """Check if dialogue is active"""
        return self.dialogue_box.active
    
    def draw(self, surface, assets):
        """Draw dialogue"""
        self.dialogue_box.draw(surface, assets)
