"""
Story content and dialogue trees for Chronicles of Aethermoor
"""

# ============================================================================
# CHAPTER 1: THE AWAKENING
# ============================================================================

DIALOGUE_VILLAGE_ELDER_INTRO = [
    {
        'speaker': 'Elder Theron',
        'text': "Aria, child... I'm glad you're safe. But I fear dark times are ahead for our village."
    },
    {
        'speaker': 'Aria',
        'text': "Elder, what's happening? The shadows in the forest... they're not natural. They attacked without warning!"
    },
    {
        'speaker': 'Elder Theron',
        'text': "No, they are not natural. The ancient texts speak of a Shadow Blight that once nearly destroyed our world. I had hoped those were just legends to frighten children..."
    },
    {
        'speaker': 'Aria',
        'text': "If it's real, how do we stop it? We can't just let it consume everything!"
    },
    {
        'speaker': 'Elder Theron',
        'text': "There is one way. Long ago, five elemental mages sealed the darkness in the Eternal Prison. Their power lives on in the Elemental Shrines scattered across Aethermoor."
    },
    {
        'speaker': 'Elder Theron',
        'text': "You must seek them out, Aria. You have the gift - I've seen your fire magic. With training, you could master all five elements."
    },
    {
        'speaker': 'Aria',
        'text': "Me? But I've barely mastered a simple fire spell! How can I possibly stop an ancient evil?"
    },
    {
        'speaker': 'Elder Theron',
        'text': "Your mother... she was one of the last great mages before the magic began to fade. She would want you to have this.",
        'choices': ['Tell me about my mother', 'I accept this burden']
    }
]

DIALOGUE_ELDER_ABOUT_MOTHER = [
    {
        'speaker': 'Elder Theron',
        'text': "Your mother, Lyra, was a guardian of the Flame Shrine. She fought bravely against the first stirrings of the Shadow Blight fifteen years ago."
    },
    {
        'speaker': 'Elder Theron',
        'text': "She gave her life sealing a breach in the magical barriers. Her staff, which I now give to you, contains a fragment of her power."
    },
    {
        'speaker': 'Aria',
        'text': "I... I won't let her sacrifice be in vain. I'll find the shrines and master the elements. For her. For everyone."
    }
]

DIALOGUE_MERCHANT_INTRO = [
    {
        'speaker': 'Merchant Gris',
        'text': "Ah, young Aria! Heading out on an adventure, are we? You'll need supplies. I have potions, equipment, and information... for the right price, of course."
    }
]

DIALOGUE_BLACKSMITH = [
    {
        'speaker': 'Blacksmith Bram',
        'text': "Heard you're going after the Shadow Blight. Brave, or foolish. Either way, you'll need better equipment. Bring me materials, I'll forge you something special."
    }
]

# ============================================================================
# CHAPTER 2: THE WIND SHRINE
# ============================================================================

DIALOGUE_WIND_SHRINE_GUARDIAN = [
    {
        'speaker': 'Spirit of Wind',
        'text': "Who dares enter the sacred Shrine of Winds? Few mortals have the courage to face the trials within."
    },
    {
        'speaker': 'Aria',
        'text': "I am Aria, daughter of Lyra. I seek the power of wind to combat the Shadow Blight!"
    },
    {
        'speaker': 'Spirit of Wind',
        'text': "Lyra... yes, I remember her. She had great respect for the old ways. Very well, prove yourself worthy and the winds shall obey your command."
    },
    {
        'speaker': 'Spirit of Wind',
        'text': "Complete the Trial of Agility. Navigate the wind currents and reach the shrine's heart. Only then will you earn my blessing."
    }
]

DIALOGUE_WIND_SHRINE_COMPLETE = [
    {
        'speaker': 'Spirit of Wind',
        'text': "Impressive! You move with the grace of the wind itself. I grant you mastery over the element of Wind."
    },
    {
        'speaker': 'Aria',  
        'text': "Thank you, honored spirit. I can feel the power flowing through me. One element down, three more to go."
    }
]

# ============================================================================
# CHAPTER 3: GATHERING POWER
# ============================================================================

DIALOGUE_ICE_SHRINE_INTRO = [
    {
        'speaker': 'Spirit of Ice',
        'text': "The temperature drops as you approach. A voice, cold as winter frost, echoes through the cavern..."
    },
    {
        'speaker': 'Spirit of Ice',
        'text': "Turn back, mortal. The power of ice is not for the weak-hearted. Only those with unwavering resolve may claim it."
    },
    {
        'speaker': 'Aria',
        'text': "I won't turn back. The Shadow Blight grows stronger each day. I need every element to stop it!"
    },
    {
        'speaker': 'Spirit of Ice',
        'text': "Then face the Trial of Endurance. Survive the frozen labyrinth and prove your determination."
    }
]

DIALOGUE_LIGHTNING_SHRINE_INTRO = [
    {
        'speaker': 'Spirit of Lightning',
        'text': "CRACK! Lightning strikes mere feet away. A voice booms like thunder..."
    },
    {
        'speaker': 'Spirit of Lightning',
        'text': "At last! A challenger! Too long have I waited for someone worthy of my power. Show me your speed, your reflexes!"
    },
    {
        'speaker': 'Aria',
        'text': "I'm ready for any challenge!"
    },
    {
        'speaker': 'Spirit of Lightning',
        'text': "Ha! Confidence! I like that. Face the Trial of Speed. Strike faster than lightning itself!"
    }
]

DIALOGUE_EARTH_SHRINE_INTRO = [
    {
        'speaker': 'Spirit of Earth',
        'text': "The ground trembles. A deep, rumbling voice speaks from the very stones..."
    },
    {
        'speaker': 'Spirit of Earth',
        'text': "Patience, young one. Earth magic is not claimed through haste. It requires understanding, connection with the land itself."
    },
    {
        'speaker': 'Aria',
        'text': "I'm willing to learn. Please, teach me."
    },
    {
        'speaker': 'Spirit of Earth',
        'text': "Then meditate upon the Trial of Strength. Move the unmovable. Shape the unshapeable. Become one with stone."
    }
]

# ============================================================================
# CHAPTER 4: THE SHADOW RISES
# ============================================================================

DIALOGUE_MYSTERIOUS_FIGURE = [
    {
        'speaker': '???',
        'text': "Well, well... the little mage has gathered quite a bit of power. Four elements already. Impressive."
    },
    {
        'speaker': 'Aria',
        'text': "Who are you? Show yourself!"
    },
    {
        'speaker': 'Shadow Lord',
        'text': "I am the Shadow Lord, the one your precious elders failed to mention. The Shadow Blight is not some mindless force - it is MY will made manifest!"
    },
    {
        'speaker': 'Aria',
        'text': "Then I'll stop you, just like the ancient mages did before!"
    },
    {
        'speaker': 'Shadow Lord',
        'text': "Those 'ancient mages' merely postponed the inevitable. My power has grown in the darkness. Even with all five elements, you cannot defeat me!"
    },
    {
        'speaker': 'Shadow Lord',
        'text': "But I'll give you a chance. Come to my citadel when you're ready. Face me... and fall like your mother did."
    },
    {
        'speaker': 'Aria',
        'text': "You... you killed my mother?!"
    },
    {
        'speaker': 'Shadow Lord',
        'text': "She was a worthy opponent. Let's see if the daughter surpasses the mother. I'll be waiting..."
    }
]

# ============================================================================
# CHAPTER 5: GATHERING ALLIES
# ============================================================================

DIALOGUE_MAGE_ACADEMY = [
    {
        'speaker': 'Archmage Valdris',
        'text': "You've mastered all five elements? Extraordinary! Not since the ancient times has anyone achieved such a feat."
    },
    {
        'speaker': 'Archmage Valdris',
        'text': "But listen carefully - the true power lies not in the individual elements, but in their combination. Unity magic."
    },
    {
        'speaker': 'Aria',
        'text': "Unity magic? I've never heard of it."
    },
    {
        'speaker': 'Archmage Valdris',
        'text': "When you combine two or more elements in harmony, their power multiplies. Fire and Wind create Firestorm. Ice and Lightning form Frozen Thunder."
    },
    {
        'speaker': 'Archmage Valdris',
        'text': "Experiment, learn the combinations. This knowledge will be crucial in your final battle against the Shadow Lord."
    }
]

DIALOGUE_KING = [
    {
        'speaker': 'King Aldric',
        'text': "Aria, the kingdoms owe you a great debt. Your quest to stop the Shadow Blight gives us all hope."
    },
    {
        'speaker': 'King Aldric',
        'text': "I'm mobilizing our forces. When you assault the Shadow Citadel, you won't face it alone. We'll create a distraction while you strike at the heart."
    },
    {
        'speaker': 'Aria',
        'text': "Thank you, Your Majesty. Together, we can end this darkness once and for all."
    }
]

# ============================================================================
# CHAPTER 6: FINAL CONFRONTATION
# ============================================================================

DIALOGUE_SHADOW_LORD_FINAL_1 = [
    {
        'speaker': 'Shadow Lord',
        'text': "You actually made it. I'm genuinely impressed. But this is where your story ends, little mage."
    },
    {
        'speaker': 'Aria',
        'text': "Not today, Shadow Lord. I've trained, I've grown, and I fight for everyone you've hurt!"
    },
    {
        'speaker': 'Shadow Lord',
        'text': "How noble. How naive. Let me show you TRUE power! Face the darkness!"
    }
]

DIALOGUE_SHADOW_LORD_PHASE_2 = [
    {
        'speaker': 'Shadow Lord',
        'text': "Impossible! How can you still stand? No matter... I'll just have to try harder!"
    },
    {
        'speaker': 'Aria',
        'text': "Give up! The light always overcomes the darkness!"
    },
    {
        'speaker': 'Shadow Lord',
        'text': "NEVER! I am eternal! I am inevitable! I am SHADOW INCARNATE!"
    }
]

DIALOGUE_SHADOW_LORD_DEFEATED = [
    {
        'speaker': 'Shadow Lord',
        'text': "No... this can't be... defeated by... a mere... child..."
    },
    {
        'speaker': 'Aria',
        'text': "Not just me. I had the strength of my friends, my teachers, and my mother guiding me."
    },
    {
        'speaker': 'Shadow Lord',
        'text': "Curse you... curse you all... but know this... darkness never truly dies... it only... waits..."
    },
    {
        'speaker': 'Aria',
        'text': "Then we'll be ready. The light will always be here to push it back."
    }
]

DIALOGUE_ENDING = [
    {
        'speaker': 'Elder Theron',
        'text': "Aria! You did it! The Shadow Blight is dissipating across the land. You've saved us all!"
    },
    {
        'speaker': 'Aria',
        'text': "We all did it together. I couldn't have succeeded without everyone's support."
    },
    {
        'speaker': 'Elder Theron',
        'text': "Your mother would be so proud of you. You've not only mastered the five elements, but you've brought hope back to Aethermoor."
    },
    {
        'speaker': 'Aria',
        'text': "This is just the beginning. I'll use this power to protect our world, to make sure the darkness never returns."
    },
    {
        'speaker': 'Elder Theron',
        'text': "And so begins a new chapter in the Chronicles of Aethermoor. The age of heroes has returned."
    },
    {
        'speaker': 'Narrator',
        'text': "And thus, Aria became known as the Elemental Guardian, protector of Aethermoor. Her legend would inspire generations to come..."
    },
    {
        'speaker': 'Narrator',
        'text': "But in the deepest shadows, something stirs, waiting for its moment to return..."
    },
    {
        'speaker': 'Narrator',
        'text': "THE END... or is it? Thank you for playing Chronicles of Aethermoor!"
    }
]

# ============================================================================
# NPC DIALOGUE
# ============================================================================

DIALOGUE_VILLAGER_1 = [
    {
        'speaker': 'Villager',
        'text': "Have you heard? Strange shadows have been appearing at night. I'm scared to leave my home after dark."
    }
]

DIALOGUE_VILLAGER_2 = [
    {
        'speaker': 'Old Woman',
        'text': "You're Lyra's daughter, aren't you? You have her eyes. She was a hero, and I believe you will be too."
    }
]

DIALOGUE_CHILD = [
    {
        'speaker': 'Child',
        'text': "Wow! Are you a real mage? Can you show me a spell? Please please please!"
    }
]

# Dialogue tree dictionary
DIALOGUE_TREES = {
    'elder_intro': DIALOGUE_VILLAGE_ELDER_INTRO,
    'elder_mother': DIALOGUE_ELDER_ABOUT_MOTHER,
    'merchant': DIALOGUE_MERCHANT_INTRO,
    'blacksmith': DIALOGUE_BLACKSMITH,
    'wind_shrine': DIALOGUE_WIND_SHRINE_GUARDIAN,
    'wind_complete': DIALOGUE_WIND_SHRINE_COMPLETE,
    'ice_shrine': DIALOGUE_ICE_SHRINE_INTRO,
    'lightning_shrine': DIALOGUE_LIGHTNING_SHRINE_INTRO,
    'earth_shrine': DIALOGUE_EARTH_SHRINE_INTRO,
    'shadow_lord_reveal': DIALOGUE_MYSTERIOUS_FIGURE,
    'mage_academy': DIALOGUE_MAGE_ACADEMY,
    'king': DIALOGUE_KING,
    'shadow_lord_fight': DIALOGUE_SHADOW_LORD_FINAL_1,
    'shadow_lord_phase2': DIALOGUE_SHADOW_LORD_PHASE_2,
    'shadow_lord_defeat': DIALOGUE_SHADOW_LORD_DEFEATED,
    'ending': DIALOGUE_ENDING,
    'villager1': DIALOGUE_VILLAGER_1,
    'villager2': DIALOGUE_VILLAGER_2,
    'child': DIALOGUE_CHILD,
}
