"""
Chronicles of Aethermoor - Main Game File
A story-driven platformer RPG with elemental magic
"""
import pygame
import sys
import random
from config import *
from utils import *
from assets_manager import assets
from camera import Camera
from player import Player
from magic_system import MagicSystem
from particle_system import ParticleSystem
from dialogue_system import DialogueManager
from ui_manager import UI_Manager
from level import LEVELS, LEVEL_ORDER
from story_data import DIALOGUE_TREES


class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Create window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        
        # Clock
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.state = STATE_MENU
        self.prev_state = STATE_MENU
        
        # Load assets
        print("Loading game assets...")
        assets.load_all_assets()
        
        # Systems
        self.camera = Camera(SCREEN_WIDTH * 4, SCREEN_HEIGHT * 2)
        self.magic_system = MagicSystem()
        self.particle_system = ParticleSystem()
        self.dialogue_manager = DialogueManager()
        self.ui_manager = UI_Manager()
        
        # Load dialogue trees
        for key, tree in DIALOGUE_TREES.items():
            self.dialogue_manager.load_dialogue_tree(key, tree)
        
        # Game entities
        self.player = None
        self.current_level = None
        self.current_level_index = 0
        
        # Story flags
        self.story_flags = {
            'met_elder': False,
            'wind_shrine_complete': False,
            'ice_shrine_complete': False,
            'lightning_shrine_complete': False,
            'earth_shrine_complete': False,
            'shadow_lord_defeated': False
        }
        
        print("Game initialized successfully!")
    
    def start_new_game(self):
        """Start a new game"""
        # Create player
        self.player = Player(100, 100)
        
        # Load first level
        self.load_level(0)
        
        # Set state to playing
        self.state = STATE_PLAYING
        
        # Show intro notification
        self.ui_manager.show_notification("Welcome to Chronicles of Aethermoor!", 3000)
    
    def load_level(self, level_index):
        """Load a level by index"""
        if level_index < 0 or level_index >= len(LEVEL_ORDER):
            return False
        
        level_key = LEVEL_ORDER[level_index]
        level_creator = LEVELS.get(level_key)
        
        if level_creator:
            self.current_level = level_creator()
            self.current_level_index = level_index
            
            # Set player position to spawn point
            self.player.pos.x, self.player.pos.y = self.current_level.spawn_point
            self.player.rect.x = int(self.player.pos.x)
            self.player.rect.y = int(self.player.pos.y)
            
            # Update camera bounds
            level_width = self.current_level.width * TILE_SIZE
            level_height = self.current_level.height * TILE_SIZE
            self.camera.set_bounds(0, 0, level_width, level_height)
            
            # Clear systems
            self.magic_system.clear()
            self.particle_system.clear()
            
            self.ui_manager.show_notification(f"Entering: {self.current_level.name}", 2000)
            
            return True
        
        return False
    
    def next_level(self):
        """Load next level"""
        next_index = self.current_level_index + 1
        if self.load_level(next_index):
            return True
        else:
            # Game completed!
            self.dialogue_manager.start_dialogue('ending')
            self.state = STATE_DIALOGUE
            return False
    
    def handle_events(self):
        """Handle game events and return them for further processing"""
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # Global pause
                if event.key == pygame.K_ESCAPE:
                    if self.state == STATE_PLAYING:
                        self.state = STATE_PAUSED
                        self.prev_state = STATE_PLAYING
                    elif self.state == STATE_PAUSED:
                        self.state = self.prev_state
                    elif self.state == STATE_DIALOGUE:
                        pass  # Can't pause during dialogue
                
                # Start game from menu
                if self.state == STATE_MENU:
                    if event.key == pygame.K_RETURN:
                        self.start_new_game()
                    elif event.key == pygame.K_q:
                        self.running = False
                
                # Resume from pause
                if self.state == STATE_PAUSED:
                    if event.key == pygame.K_r:
                        self.state = self.prev_state
                    elif event.key == pygame.K_q:
                        self.state = STATE_MENU
                
                # Game over
                if self.state == STATE_GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        self.state = STATE_MENU
                
                # Interact with NPCs
                if self.state == STATE_PLAYING and event.key == pygame.K_e:
                    interactable_npc = None
                    for npc in self.current_level.npcs:
                        if npc.can_interact_with(self.player):
                            interactable_npc = npc
                            break
                    
                    if interactable_npc:
                        dialogue_key = interactable_npc.dialogue_key
                        if self.dialogue_manager.start_dialogue(dialogue_key):
                            self.state = STATE_DIALOGUE
                            self.prev_state = STATE_PLAYING
            
            # Menu mouse interactions (outside KEYDOWN block!)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == STATE_MENU:
                    mouse_pos = event.pos
                    # Simple click detection for "Start New Game"
                    start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 350 - 20, 300, 50)
                    quit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 490 - 20, 300, 50)
                    
                    if start_rect.collidepoint(mouse_pos):
                        self.start_new_game()
                    elif quit_rect.collidepoint(mouse_pos):
                        self.running = False
                
                # Pause menu mouse interactions
                elif self.state == STATE_PAUSED:
                    mouse_pos = event.pos
                    # Button positions match draw_pause_menu
                    resume_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, 200, 40)
                    restart_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 30, 200, 40)
                    menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80, 200, 40)
                    quit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 130, 200, 40)
                    
                    if resume_rect.collidepoint(mouse_pos):
                        self.state = self.prev_state
                    elif restart_rect.collidepoint(mouse_pos):
                        # Restart current level
                        self.load_level(self.current_level_index)
                        self.state = STATE_PLAYING
                    elif menu_rect.collidepoint(mouse_pos):
                        self.state = STATE_MENU
                    elif quit_rect.collidepoint(mouse_pos):
                        self.running = False
        
        return events
    
    def update(self, dt, events):
        """Update game logic"""
        # Update UI
        self.ui_manager.update(dt)
        
        if self.state == STATE_MENU:
            # Menu animations could go here
            pass
        
        elif self.state == STATE_PLAYING:
            if self.player and self.current_level:
                # Get input
                keys = pygame.key.get_pressed()
                
                # Handle player input
                cast_spell = self.player.handle_input(keys, events)
                
                # Create spell if player cast one
                if cast_spell:
                    spell_x = self.player.rect.centerx + (30 if self.player.facing_right else -30)
                    spell_y = self.player.rect.centery
                    self.magic_system.create_spell(spell_x, spell_y, 
                                                  self.player.facing_right, 
                                                  cast_spell, 'player')
                    
                    # Particle effect
                    self.particle_system.create_magic_cast(
                        (self.player.rect.centerx, self.player.rect.centery),
                        cast_spell
                    )
                
                # Update player
                self.player.update(dt, self.current_level.tilemap.solid_tiles)
                
                # Update level
                self.current_level.update(dt, self.player)
                
                # Update magic system
                self.magic_system.update(dt, self.current_level.tilemap.solid_tiles)
                
                # Check spell hits on enemies
                for enemy in self.current_level.enemies[:]:
                    hits = self.magic_system.check_hits(enemy.rect, 'player')
                    for spell in hits:
                        if enemy.take_damage(spell.damage):
                            # Enemy died
                            self.particle_system.create_explosion(
                                (enemy.rect.centerx, enemy.rect.centery),
                                GRAY
                            )
                            self.camera.shake(3, 150)
                
                # Check spell hits on bosses
                for boss in self.current_level.bosses[:]:
                    hits = self.magic_system.check_hits(boss.rect, 'player')
                    for spell in hits:
                        if boss.take_damage(spell.damage):
                            # Boss died
                            self.particle_system.create_explosion(
                                (boss.rect.centerx, boss.rect.centery),
                                PURPLE
                            )
                            self.camera.shake(10, 500)
                            self.ui_manager.show_notification("Boss Defeated!", 3000)
                            
                            # Spawn exit portal for boss levels
                            if not self.current_level.exit_portal:
                                portal_x = boss.rect.centerx + 200
                                portal_y = boss.rect.y
                                self.current_level.exit_portal = pygame.Rect(portal_x, portal_y, 64, 100)
                                self.ui_manager.show_notification("Exit Portal Appeared!", 2000)
                
                # Check player melee hits
                attack_rect = self.player.get_attack_rect()
                if attack_rect:
                    for enemy in self.current_level.enemies[:]:
                        if attack_rect.colliderect(enemy.rect):
                            if enemy.take_damage(self.player.attack_damage):
                                self.particle_system.create_explosion(
                                    (enemy.rect.centerx, enemy.rect.centery),
                                    GRAY
                                )
                                self.camera.shake(2, 100)
                    
                    for boss in self.current_level.bosses[:]:
                        if attack_rect.colliderect(boss.rect):
                            boss.take_damage(self.player.attack_damage)
                            self.camera.shake(3, 150)
                
                # Update camera
                self.camera.follow(self.player.rect)
                self.camera.update(dt)
                
                # Update particle system
                self.particle_system.update(dt)
                
                # Check level completion
                if self.current_level.completed:
                    # Show completion message and move to next level
                    self.ui_manager.show_notification("Level Complete!", 2000)
                    pygame.time.delay(2000)
                    self.next_level()
                
                # Check player death
                if self.player.hp <= 0:
                    self.state = STATE_GAME_OVER
        
        elif self.state == STATE_DIALOGUE:
            # Update dialogue
            result = self.dialogue_manager.update(dt, events)
            
            if result:
                event_type, data = result
                if event_type == 'complete':
                    # Dialogue finished
                    self.state = self.prev_state
                elif event_type == 'choice':
                    # Handle player choice
                    if data == 'Tell me about my mother':
                        self.dialogue_manager.start_dialogue('elder_mother')
                    elif data == 'I accept this burden':
                        self.story_flags['met_elder'] = True
                        self.state = self.prev_state
        
        elif self.state == STATE_PAUSED:
            # Nothing to update when paused
            pass
        
        elif self.state == STATE_GAME_OVER:
            # Nothing to update
            pass
    
    def render(self):
        """Render game"""
        self.screen.fill(BLACK)
        
        if self.state == STATE_MENU:
            self.ui_manager.draw_main_menu(self.screen, assets)
        
        elif self.state in [STATE_PLAYING, STATE_DIALOGUE, STATE_PAUSED]:
            if self.current_level:
                # Draw level
                self.current_level.draw(self.screen, self.camera, assets)
            
            # Draw player
            if self.player:
                self.player.draw(self.screen, self.camera)
            
            # Draw magic
            self.magic_system.draw(self.screen, self.camera)
            
            # Draw particles
            self.particle_system.draw(self.screen, self.camera)
            
            # Draw HUD
            if self.player:
                self.ui_manager.draw_hud(self.screen, self.player, assets)
            
            # Draw dialogue if active
            if self.state == STATE_DIALOGUE:
                self.dialogue_manager.draw(self.screen, assets)
            
            # Draw pause menu
            if self.state == STATE_PAUSED:
                self.ui_manager.draw_pause_menu(self.screen, assets)
        
        elif self.state == STATE_GAME_OVER:
            self.ui_manager.draw_game_over(self.screen, assets)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("Starting game loop...")
        
        while self.running:
            # Get delta time
            dt = self.clock.tick(FPS)
            
            # Handle events
            events = self.handle_events()
            
            # Update
            self.update(dt, events)
            
            # Render
            self.render()
        
        # Cleanup
        pygame.quit()
        sys.exit()


def main():
    """Main entry point"""
    print("=" * 60)
    print("Chronicles of Aethermoor")
    print("A Story-Driven Platformer RPG")
    print("=" * 60)
    print()
    
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
