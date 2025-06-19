from typing import Any
import os
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("smh_huddle_recordings")
API_BASE_URL = os.getenv("API_BASE_URL").rstrip("/")
API_KEY = os.getenv("API_KEY")


@mcp.tool()
async def list_recordings(skip: int = 0, limit: int = 10, period: str = None) -> str:
    """
    Get a list of huddle (call) recordings

    Hints:  
    - Recordings are sorted by date in descending order, so if you want to get the most recent recording, just set limit to 1
    - Use the "tldr" field to quickly understand the context of the recording, but never rely on it if the user asks for a summary of the recording. For creating a summary refer to the diarized transcript of the recording by using the get_recording tool

    Args:
        skip: int - number of recordings to skip (default: 0)
        limit: int - number of recordings to return (default: 10)
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/recordings",
                headers={"X-API-Key": API_KEY},
                params={"skip": skip, "limit": limit, "simplified": True}
            )
            return response.text
    except Exception as e:
        return f"Request error: {e}"


@mcp.tool()
async def get_recording(recording_id: str) -> str:
    """
    Get a recording by its ID

    Hints:
    - Try to use this tool not more than 7 times throughout one conversation
    - When creating a summary, refer to the diarized transcript
    - Use this guideline to create an effective summary:
        Goal: quickly get a transparent picture of the team's progress, identify blockers and deviations from the plan for decision-making.
        Task: based on the text of the recording, generate a summary for each participant (with specifics, without missing details) in the format:
        <Name>
        What was done yesterday:
        - …
        Problems:
        - …
        Plans:
        - …
        Agreements (if there were none, do not indicate this item):
        - …
        Translate your answer to the user's language
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/recordings/{recording_id}",
                headers={"X-API-Key": API_KEY},
                params={"simplified": True}
            )
            return response.text
    except Exception as e:
        return f"Request error: {e}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
