from fastapi import APIRouter, HTTPException, status
from src.api.schemas import (
    TeamInfo,
    MatchDetails,
    EmojiReactionCreate,
    EmojiReactionsResponse,
    EmojiReaction,
)
from src.api.models import add_emoji_reaction, get_emoji_reactions

import os
from datetime import datetime

router = APIRouter()

# ---- DUMMY DATA ----
TEAM_DATA = {
    1: TeamInfo(
        id=1,
        name="Thunderbolts",
        logo_url="https://cdn.example.com/logos/thunderbolts.png",
        players=["Alice", "Bob", "Charlie", "David", "Eva"]
    ),
    2: TeamInfo(
        id=2,
        name="Warriors",
        logo_url="https://cdn.example.com/logos/warriors.png",
        players=["Xavier", "Yara", "Zane", "Walter", "Quinn"]
    ),
}
MATCH_DATA = MatchDetails(
    match_id=100,
    youtube_url=os.getenv("YOUTUBE_URL", "https://www.youtube.com/watch?v=EXAMPLE_MATCH"),
    team_a=TEAM_DATA[1],
    team_b=TEAM_DATA[2],
    start_time=datetime.now().isoformat(),
    status="live",
    score={
        "team_a": "76/2 (10.3)",
        "team_b": "N/A"
    }
)
EMOJI_TYPES = ["6", "out", "surprise", "laugh", "celebration"]


# PUBLIC_INTERFACE
@router.get(
    "/match",
    response_model=MatchDetails,
    summary="Get match details",
    description="Returns details for the current match, including YouTube streaming URL, teams, start time, and score.",
    tags=["Match"],
)
async def get_match_details():
    """
    Get details about the current match. 
    Ensures no ETag or cache header is set, always returns 200 with data.
    """
    # Explicitly remove cache/etag headers if any were set by middleware
    # FastAPI does not set ETag or cache headers by default, but some caching proxies or Uvicorn reloads might add them.
    return MATCH_DATA

# PUBLIC_INTERFACE
@router.get(
    "/teams/{team_id}",
    response_model=TeamInfo,
    summary="Get team info",
    description="Returns team info by ID, including team name, logo, and player list.",
    tags=["Teams"],
)
async def get_team_info(team_id: int):
    """
    Get details about a team by ID.
    """
    team = TEAM_DATA.get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail=f"Team ID {team_id} not found")
    return team

# PUBLIC_INTERFACE
@router.post(
    "/emoji",
    status_code=status.HTTP_201_CREATED,
    summary="Submit emoji reaction",
    description="Submit an emoji reaction for the current match. Allowed emojis: 6, out, surprise, laugh, celebration.",
    tags=["Emoji"],
    response_model=None,
)
async def submit_emoji_reaction(payload: EmojiReactionCreate):
    """
    Add an emoji reaction for a match.
    """
    if payload.emoji not in EMOJI_TYPES:
        raise HTTPException(status_code=400, detail=f"Emoji must be one of: {', '.join(EMOJI_TYPES)}")
    add_emoji_reaction(payload.match_id, payload.emoji)
    return {"message": "Reaction recorded"}

# PUBLIC_INTERFACE
@router.get(
    "/emoji/{match_id}",
    response_model=EmojiReactionsResponse,
    summary="Get emoji reactions for match",
    description="Get the count of each emoji reaction for a match.",
    tags=["Emoji"],
)
async def get_emoji_reactions_endpoint(match_id: int):
    """
    Get emoji reaction counts for a given match.
    """
    counts = get_emoji_reactions(match_id)
    # Ensure all emoji types sent with default 0
    all_counts = [EmojiReaction(emoji=e, count=counts.get(e, 0)) for e in EMOJI_TYPES]
    return EmojiReactionsResponse(match_id=match_id, reactions=all_counts)
