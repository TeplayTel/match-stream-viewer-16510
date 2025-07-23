from typing import Dict
from threading import Lock


# In-memory store for emoji reactions: {match_id: {emoji: count, ...}, ...}
EMOJI_STORE: Dict[int, Dict[str, int]] = {}
STORE_LOCK = Lock()


def add_emoji_reaction(match_id: int, emoji: str):
    """Store an emoji reaction for the given match."""
    with STORE_LOCK:
        if match_id not in EMOJI_STORE:
            EMOJI_STORE[match_id] = {}
        if emoji not in EMOJI_STORE[match_id]:
            EMOJI_STORE[match_id][emoji] = 0
        EMOJI_STORE[match_id][emoji] += 1


def get_emoji_reactions(match_id: int) -> Dict[str, int]:
    """Retrieve emoji reactions for the given match."""
    with STORE_LOCK:
        return dict(EMOJI_STORE.get(match_id, {}))
