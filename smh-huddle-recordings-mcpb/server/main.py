#!/usr/bin/env python3
"""
SMH Huddle Recordings MCP Server
Desktop Extension for accessing and analyzing huddle recordings
"""

import os
import sys
import json
import logging
import asyncio
from typing import Any, Optional
from datetime import datetime

# Add vendor directory to Python path for bundled dependencies
vendor_dir = os.path.join(os.path.dirname(__file__), 'vendor')
if os.path.exists(vendor_dir):
    sys.path.insert(0, vendor_dir)

import httpx
from mcp.server.fastmcp import FastMCP

# Initialize logging
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr if DEBUG else open(os.devnull, 'w')
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("smh-huddle-recordings")

# Configuration with validation
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")

# Validate required environment variables
if not API_BASE_URL:
    logger.error("API_BASE_URL environment variable is not set")
    sys.exit(1)

if not API_KEY:
    logger.error("API_KEY environment variable is not set")
    sys.exit(1)

# Clean up API base URL
API_BASE_URL = API_BASE_URL.rstrip("/")
logger.info(f"Initialized SMH Huddle Recordings server with API: {API_BASE_URL[:30]}...")

# HTTP client configuration
DEFAULT_TIMEOUT = 30.0  # 30 seconds timeout for API calls
MAX_RETRIES = 3


async def make_api_request(
    method: str,
    endpoint: str,
    params: Optional[dict] = None,
    timeout: float = DEFAULT_TIMEOUT
) -> dict:
    """
    Make an API request with proper error handling and retries

    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint path
        params: Query parameters
        timeout: Request timeout in seconds

    Returns:
        Parsed JSON response

    Raises:
        Various exceptions with descriptive error messages
    """
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"X-API-Key": API_KEY}

    logger.debug(f"Making {method} request to {url}")

    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params
                )

                # Check for successful response
                response.raise_for_status()

                # Parse and return JSON
                data = response.json()
                logger.debug(f"Request successful, received {len(str(data))} bytes")
                return data

        except httpx.TimeoutException:
            logger.warning(f"Request timeout (attempt {attempt + 1}/{MAX_RETRIES})")
            if attempt == MAX_RETRIES - 1:
                raise Exception(f"Request timed out after {timeout} seconds. The API server may be slow or unreachable.")

        except httpx.HTTPStatusError as e:
            error_msg = f"API returned error status {e.response.status_code}"
            try:
                error_data = e.response.json()
                if "message" in error_data:
                    error_msg += f": {error_data['message']}"
            except:
                error_msg += f": {e.response.text[:200]}"
            logger.error(error_msg)
            raise Exception(error_msg)

        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise Exception(f"Failed to connect to API: {str(e)}")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse API response as JSON: {e}")
            raise Exception("API returned invalid JSON response")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise Exception(f"Unexpected error occurred: {str(e)}")

        # Wait before retry
        if attempt < MAX_RETRIES - 1:
            await asyncio.sleep(2 ** attempt)  # Exponential backoff

    raise Exception("Failed to complete request after all retries")


@mcp.tool()
async def list_recordings(
    skip: int = 0,
    limit: int = 10,
    period: Optional[str] = None
) -> str:
    """
    Get a list of huddle (call) recordings

    Recordings are sorted by date in descending order (newest first).
    Use the "tldr" field for quick context, but create proper summaries
    from the full transcript using get_recording.

    Args:
        skip: Number of recordings to skip for pagination (default: 0)
        limit: Number of recordings to return, max 100 (default: 10)
        period: Optional time period filter (e.g., "today", "week", "month")

    Returns:
        JSON string containing the list of recordings with metadata
    """
    try:
        # Validate parameters
        if skip < 0:
            return json.dumps({
                "error": "Invalid parameter",
                "message": "skip must be non-negative"
            })

        if limit < 1 or limit > 100:
            return json.dumps({
                "error": "Invalid parameter",
                "message": "limit must be between 1 and 100"
            })

        # Build query parameters
        params = {
            "skip": skip,
            "limit": limit,
            "simplified": True
        }

        if period:
            params["period"] = period

        logger.info(f"Fetching recordings list (skip={skip}, limit={limit}, period={period})")

        # Make API request
        data = await make_api_request("GET", "/recordings", params=params)

        # Return formatted response
        return json.dumps(data, indent=2, ensure_ascii=False)

    except Exception as e:
        error_response = {
            "error": "Failed to fetch recordings",
            "message": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
        logger.error(f"list_recordings failed: {e}")
        return json.dumps(error_response, indent=2)


@mcp.tool()
async def get_recording(recording_id: str) -> str:
    """
    Get detailed information about a specific recording

    Returns the full diarized transcript and metadata for a recording.
    Use this for creating summaries following the standard format:
    - What was done yesterday
    - Problems encountered
    - Future plans
    - Agreements reached

    Note: Limit usage to ~7 calls per conversation for performance.

    Args:
        recording_id: Unique identifier of the recording

    Returns:
        JSON string containing full recording details and transcript
    """
    try:
        # Validate recording ID
        if not recording_id or not recording_id.strip():
            return json.dumps({
                "error": "Invalid parameter",
                "message": "recording_id is required and cannot be empty"
            })

        recording_id = recording_id.strip()
        logger.info(f"Fetching recording details for ID: {recording_id}")

        # Make API request with extended timeout for large transcripts
        data = await make_api_request(
            "GET",
            f"/recordings/{recording_id}",
            params={"simplified": True},
            timeout=60.0  # Longer timeout for detailed recordings
        )

        # Add usage hint to response
        if isinstance(data, dict) and "transcript" in data:
            data["_usage_hint"] = (
                "Create summaries from the diarized transcript. "
                "Format: Name, What was done, Problems, Plans, Agreements"
            )

        # Return formatted response
        return json.dumps(data, indent=2, ensure_ascii=False)

    except Exception as e:
        error_response = {
            "error": "Failed to fetch recording",
            "message": str(e),
            "recording_id": recording_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        logger.error(f"get_recording failed for {recording_id}: {e}")
        return json.dumps(error_response, indent=2)


# Server startup
if __name__ == "__main__":
    try:
        logger.info("Starting SMH Huddle Recordings MCP server...")
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)