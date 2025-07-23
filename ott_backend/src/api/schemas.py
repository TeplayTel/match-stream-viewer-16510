from pydantic import BaseModel, Field
from typing import List, Optional, Dict


# PUBLIC_INTERFACE
class TeamInfo(BaseModel):
    """Information about a team."""
    id: int = Field(..., description="Team unique identifier")
    name: str = Field(..., description="Name of the team")
    logo_url: Optional[str] = Field(None, description="URL for the team's logo")
    players: List[str] = Field(..., description="List of player names in the team")

# PUBLIC_INTERFACE
class MatchDetails(BaseModel):
    """Details for the current match."""
    match_id: int = Field(..., description="Match unique identifier")
    youtube_url: str = Field(..., description="YouTube URL for live streaming")
    team_a: TeamInfo = Field(..., description="Details for Team A")
    team_b: TeamInfo = Field(..., description="Details for Team B")
    start_time: str = Field(..., description="ISO8601 start time of the match")
    status: str = Field(..., description="Match status e.g. 'live', 'completed', 'upcoming'")
    score: Dict[str, str] = Field(..., description="Current score: keys are 'team_a', 'team_b'")

# PUBLIC_INTERFACE
class EmojiReactionCreate(BaseModel):
    """Payload for submitting an emoji reaction."""
    match_id: int = Field(..., description="Match unique identifier")
    emoji: str = Field(..., description="The type of emoji (6, out, surprise, laugh, celebration)")

# PUBLIC_INTERFACE
class EmojiReaction(BaseModel):
    """Represents an emoji reaction record."""
    emoji: str = Field(..., description="The type of emoji")
    count: int = Field(..., description="Number of times this emoji was used")

# PUBLIC_INTERFACE
class EmojiReactionsResponse(BaseModel):
    """Response containing counts of emoji reactions."""
    match_id: int = Field(..., description="Match unique identifier")
    reactions: List[EmojiReaction] = Field(..., description="List of emoji reactions and their counts")
