"""
Game Configuration and Constants
Chronicles of Aethermoor
"""

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Chronicles of Aethermoor"

# Game settings
TILE_SIZE = 32
GRAVITY = 0.8
MAX_FALL_SPEED = 20

# Player settings
PLAYER_SPEED = 5
PLAYER_JUMP_POWER = 18
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = 0.8
PLAYER_MAX_HP = 100
PLAYER_MAX_MP = 100
PLAYER_ATTACK_COOLDOWN = 300  # milliseconds
PLAYER_INVINCIBILITY_TIME = 1000  # milliseconds after hit

# Magic settings
SPELL_COOLDOWN = 500  # milliseconds
FIRE_SPELL_COST = 15
ICE_SPELL_COST = 20
LIGHTNING_SPELL_COST = 25
EARTH_SPELL_COST = 18
WIND_SPELL_COST = 12

# Camera settings
CAMERA_SPEED = 0.1
CAMERA_DEADZONE_X = 200
CAMERA_DEADZONE_Y = 150

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
DARK_RED = (139, 0, 0)
GREEN = (50, 220, 50)
BLUE = (50, 120, 220)
DARK_BLUE = (25, 60, 110)
YELLOW = (255, 220, 50)
ORANGE = (255, 150, 50)
PURPLE = (180, 50, 220)
CYAN = (50, 220, 220)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (180, 180, 180)

# UI Colors
UI_BG_COLOR = (20, 20, 40, 200)  # Semi-transparent dark blue
UI_BORDER_COLOR = (100, 150, 255)
UI_TEXT_COLOR = WHITE
UI_HIGHLIGHT_COLOR = YELLOW
HP_BAR_COLOR = (220, 50, 50)
MP_BAR_COLOR = (50, 120, 220)
XP_BAR_COLOR = (255, 215, 0)

# Rendering layers (lower = background, higher = foreground)
LAYER_BACKGROUND = 0
LAYER_TILES = 1
LAYER_ITEMS = 2
LAYER_ENEMIES = 3
LAYER_PLAYER = 4
LAYER_EFFECTS = 5
LAYER_UI = 6

# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_DIALOGUE = "dialogue"
STATE_INVENTORY = "inventory"
STATE_CUTSCENE = "cutscene"
STATE_GAME_OVER = "game_over"

# Element types for magic
ELEMENT_FIRE = "fire"
ELEMENT_ICE = "ice"
ELEMENT_LIGHTNING = "lightning"
ELEMENT_EARTH = "earth"
ELEMENT_WIND = "wind"

# Direction constants
DIR_LEFT = "left"
DIR_RIGHT = "right"
DIR_UP = "up"
DIR_DOWN = "down"

# Save file
SAVE_DIRECTORY = "saves"
MAX_SAVE_SLOTS = 3
