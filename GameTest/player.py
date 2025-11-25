"""
Player character implementation
"""
import pygame
from config import *
from utils import Timer, Vector2, create_placeholder_surface
from assets_manager import assets

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Position and physics
        self.pos = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.rect = pygame.Rect(x, y, 48, 64)
        
        # Movement
        self.speed = PLAYER_SPEED
        self.jump_power = PLAYER_JUMP_POWER
        self.on_ground = False
        self.facing_right = True
        
        # Combat
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp
        self.max_mp = PLAYER_MAX_MP
        self.mp = self.max_mp
        self.attack_damage = 15
        self.is_attacking = False
        self.is_casting = False
        self.attack_timer = Timer(PLAYER_ATTACK_COOLDOWN)
        self.invincible = False
        self.invincible_timer = Timer(PLAYER_INVINCIBILITY_TIME)
        
        # Stats
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        
        # Magic
        self.unlocked_spells = [ELEMENT_FIRE]  # Start with fire
        self.selected_spell = ELEMENT_FIRE
        self.spell_cooldown = Timer(SPELL_COOLDOWN)
        
        # Animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 100  # ms per frame
        self.state = 'idle'
        
        # Inventory
        self.inventory = {}
        self.gold = 0
        
        # Input buffer
        self.input_buffer = {
            'jump': False,
            'attack': False,
            'cast': False
        }
    
    def handle_input(self, keys, events):
        """Handle player input"""
        # Movement
        move_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = -1
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = 1
            self.facing_right = True
        
        self.velocity.x = move_x * self.speed
        
        # Jump (buffered input)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                    self.input_buffer['jump'] = True
                elif event.key in [pygame.K_j, pygame.K_z]:
                    self.input_buffer['attack'] = True
                elif event.key in [pygame.K_k, pygame.K_x]:
                    self.input_buffer['cast'] = True
                
                # Spell selection
                elif event.key == pygame.K_1 and ELEMENT_FIRE in self.unlocked_spells:
                    self.selected_spell = ELEMENT_FIRE
                elif event.key == pygame.K_2 and ELEMENT_ICE in self.unlocked_spells:
                    self.selected_spell = ELEMENT_ICE
                elif event.key == pygame.K_3 and ELEMENT_LIGHTNING in self.unlocked_spells:
                    self.selected_spell = ELEMENT_LIGHTNING
                elif event.key == pygame.K_4 and ELEMENT_EARTH in self.unlocked_spells:
                    self.selected_spell = ELEMENT_EARTH
                elif event.key == pygame.K_5 and ELEMENT_WIND in self.unlocked_spells:
                    self.selected_spell = ELEMENT_WIND
        
        # Process jump buffer
        if self.input_buffer['jump'] and self.on_ground:
            self.velocity.y = -self.jump_power
            self.on_ground = False
            self.input_buffer['jump'] = False
        
        # Process attack buffer
        if self.input_buffer['attack'] and not self.attack_timer.is_active():
            self.attack()
            self.input_buffer['attack'] = False
        
        # Process cast buffer
        if self.input_buffer['cast'] and not self.spell_cooldown.is_active():
            spell = self.cast_spell()  # Return spell to be created
            self.input_buffer['cast'] = False  # Clear buffer after casting
            return spell
        
        return None
    
    def attack(self):
        """Perform melee attack"""
        self.is_attacking = True
        self.state = 'attack'
        self.animation_frame = 0
        self.attack_timer.start()
    
    def cast_spell(self):
        """Cast selected spell"""
        spell_costs = {
            ELEMENT_FIRE: FIRE_SPELL_COST,
            ELEMENT_ICE: ICE_SPELL_COST,
            ELEMENT_LIGHTNING: LIGHTNING_SPELL_COST,
            ELEMENT_EARTH: EARTH_SPELL_COST,
            ELEMENT_WIND: WIND_SPELL_COST
        }
        
        cost = spell_costs.get(self.selected_spell, 15)
        
        if self.mp >= cost:
            self.mp -= cost
            self.is_casting = True
            self.state = 'cast'
            self.animation_frame = 0
            self.spell_cooldown.start()
            return self.selected_spell
        
        return None
    
    def update(self, dt, tiles):
        """Update player state"""
        # Update timers
        if self.attack_timer.update():
            self.is_attacking = False
        
        if self.invincible_timer.update():
            self.invincible = False
        
        self.spell_cooldown.update()
        
        # Apply gravity
        if not self.on_ground:
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
        self.update_animation(dt)
        
        # Regenerate mana slowly
        if self.mp < self.max_mp:
            self.mp = min(self.mp + 0.05, self.max_mp)
    
    def handle_collision_x(self, tiles):
        """Handle horizontal collisions"""
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.velocity.x > 0:  # Moving right
                    self.rect.right = tile.rect.left
                elif self.velocity.x < 0:  # Moving left
                    self.rect.left = tile.rect.right
                self.pos.x = self.rect.x
                self.velocity.x = 0
    
    def handle_collision_y(self, tiles):
        """Handle vertical collisions"""
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.velocity.y > 0:  # Falling
                    self.rect.bottom = tile.rect.top
                    self.on_ground = True
                    self.velocity.y = 0
                elif self.velocity.y < 0:  # Jumping up
                    self.rect.top = tile.rect.bottom
                    self.velocity.y = 0
                self.pos.y = self.rect.y
    
    def update_animation(self, dt):
        """Update animation state and frame"""
        # Determine state
        if self.is_attacking:
            self.state = 'attack'
        elif self.is_casting:
            self.state = 'cast'
        elif not self.on_ground:
            if self.velocity.y < 0:
                self.state = 'jump'
            else:
                self.state = 'fall'
        elif abs(self.velocity.x) > 0:
            self.state = 'walk'
        else:
            self.state = 'idle'
        
        # Update animation timer
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            
            # Update frame based on state
            if self.state == 'walk':
                self.animation_frame = (self.animation_frame + 1) % 6
            elif self.state in ['attack', 'cast']:
                self.animation_frame += 1
                if self.animation_frame >= 4:
                    self.animation_frame = 0
                    if self.state == 'attack':
                        self.is_attacking = False
                    elif self.state == 'cast':
                        self.is_casting = False
            else:
                self.animation_frame = 0
    
    def take_damage(self, damage):
        """Take damage from enemy"""
        if not self.invincible:
            self.hp = max(0, self.hp - damage)
            self.invincible = True
            self.invincible_timer.start()
            return True
        return False
    
    def heal(self, amount):
        """Heal player"""
        self.hp = min(self.hp + amount, self.max_hp)
    
    def restore_mana(self, amount):
        """Restore mana"""
        self.mp = min(self.mp + amount, self.max_mp)
    
    def gain_experience(self, amount):
        """Gain experience points"""
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level_up()
    
    def level_up(self):
        """Level up the player"""
        self.level += 1
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)
        
        # Increase stats
        self.max_hp += 10
        self.hp = self.max_hp
        self.max_mp += 10
        self.mp = self.max_mp
        self.attack_damage += 3
    
    def unlock_spell(self, element):
        """Unlock a new spell"""
        if element not in self.unlocked_spells:
            self.unlocked_spells.append(element)
    
    def get_attack_rect(self):
        """Get attack hitbox"""
        if self.is_attacking:
            if self.facing_right:
                return pygame.Rect(self.rect.right, self.rect.y, 32, self.rect.height)
            else:
                return pygame.Rect(self.rect.left - 32, self.rect.y, 32, self.rect.height)
        return None
    
    def draw(self, surface, camera):
        """Draw player"""
        screen_pos = camera.apply(self.rect)
        
        # Get current sprite
        player_sprites = assets.images.get('player', {})
        
        if self.state == 'walk' and 'walk' in player_sprites:
            sprite = player_sprites['walk'][self.animation_frame % len(player_sprites['walk'])]
        elif self.state == 'attack' and 'attack' in player_sprites:
            sprite = player_sprites['attack'][self.animation_frame % len(player_sprites['attack'])]
        elif self.state == 'cast' and 'cast' in player_sprites:
            sprite = player_sprites['cast'][self.animation_frame % len(player_sprites['cast'])]
        elif self.state in player_sprites:
            sprite = player_sprites[self.state]
        else:
            sprite = player_sprites.get('idle', create_placeholder_surface(48, 64, BLUE))
        
        # Flip if facing left
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        # Flash when invincible
        if self.invincible and (pygame.time.get_ticks() // 100) % 2:
            sprite = sprite.copy()
            sprite.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_MULT)
        
        surface.blit(sprite, screen_pos)
        
        # Debug hitbox
        # pygame.draw.rect(surface, RED, screen_pos, 1)
