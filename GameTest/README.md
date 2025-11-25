# Chronicles of Aethermoor

A story-driven platformer RPG inspired by Phoenotopia Awakening, featuring elemental magic, boss battles, and an epic narrative.

## Story

In the mystical land of Aethermoor, darkness stirs. Aria, a young mage apprentice, must master the five elemental magics and confront the Shadow Lord to save her world from the ancient Shadow Blight.

## Features

- **Epic Story**: 6-chapter narrative with rich dialogue and character development
- **5 Elemental Magic System**: Master Fire, Ice, Lightning, Earth, and Wind
- **Multiple Areas**: Explore village, forest, shrines, caves, and the Shadow Citadel
- **Boss Battles**: Face 3 epic bosses with unique phases and mechanics
- **NPC Interactions**: Talk with villagers, merchants, and quest givers
- **Level Progression**: Gain experience, level up, and unlock new spells
- **Combat System**: Combine melee staff attacks with powerful magic
- **Particle Effects**: Beautiful visual effects for magic and combat

## Controls

- **WASD / Arrow Keys**: Movement
- **Space**: Jump
- **J / Z**: Melee Attack
- **K / X**: Cast Selected Spell
- **1-5**: Select Spell (Fire, Ice, Lightning, Earth, Wind)
- **E**: Interact with NPCs
- **ESC**: Pause Game
- **Enter**: Confirm/Start

## Installation

### Requirements

```bash
pip install pygame
```

### Running the Game

```bash
python main.py
```

## Game Structure

```
GameTest/
├── main.py                 # Main game file
├── config.py              # Game configuration and constants
├── utils.py               # Utility functions and classes
├── assets_manager.py      # Asset loading and management
├── camera.py              # Camera system
├── player.py              # Player character
├── enemy.py               # Enemy AI and behaviors
├── boss.py                # Boss battles
├── npc.py                 # NPC system
├── magic_system.py        # Magic and spells
├── particle_system.py     # Visual effects
├── dialogue_system.py     # Dialogue and story
├── tiles.py               # Tile system
├── level.py               # Level creation
├── ui_manager.py          # UI and HUD
└── story_data.py          # Story content and dialogue
```

## Story Chapters

1. **The Awakening**: Aria discovers her powers and learns of the Shadow Blight
2. **The Wind Shrine**: Master the element of Wind
3. **Gathering Power**: Unlock Ice, Lightning, and Earth magic
4. **The Shadow Rises**: Confront the Shadow Lord's revelation
5. **Gathering Allies**: Unite the kingdoms
6. **Final Confrontation**: Face the Shadow Lord in epic battle

## Magic System

### Elements
- **Fire**: High damage, burning effect
- **Ice**: Freezing enemies, slowing effects
- **Lightning**: Fastest projectile, stunning
- **Earth**: Highest damage, slow but powerful
- **Wind**: Fast, knockback effect

### Spell Combinations
Combine elements for more powerful effects:
- Fire + Wind = Firestorm
- Ice + Lightning = Frozen Thunder
- Earth + Fire = Lava
- And more!

## Credits

**Game Design & Programming**: Created with Claude (Antigravity)
**Engine**: Pygame
**Art**: Placeholder pixel art (replace with your own assets)
**Inspired By**: Phoenotopia Awakening

## License

This game is a demo/learning project. Feel free to modify and learn from the code.

## Future Enhancements

- Custom pixel art assets
- Sound effects and music
- Save/Load system
- More levels and areas
- Additional enemy types
- Crafting system
- Side quests
- Achievement system

## Tips for Playing

- Talk to all NPCs for story context and hints
- Experiment with different spell combinations
- Level up before boss battles
- Explore thoroughly for hidden areas
- Use the right element for different enemies

Enjoy your adventure in Aethermoor!
