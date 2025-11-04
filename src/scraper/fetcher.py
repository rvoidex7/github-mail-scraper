"""Fetch .patch URLs with retry logic"""
import asyncio
from typing import Optional
import httpx


async def fetch_patch(
    url: str,
    token: Optional[str] = None,
    max_retries: int = 3,
    timeout: float = 30.0,
) -> str:
    """Fetch .patch content from a URL with exponential backoff on transient errors.
    
    Args:
        url: Full URL to the .patch (e.g. https://github.com/owner/repo/pull/123.patch)
        token: Optional GitHub token for Authorization header
        max_retries: Maximum retry attempts
        timeout: Request timeout in seconds
    
    Returns:
        The raw patch text (str)
    
    Raises:
        httpx.HTTPStatusError for non-retryable 4xx errors
        httpx.RequestError for network/timeout errors after retries exhausted
    """
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(max_retries):
            try:
                resp = await client.get(url, headers=headers, follow_redirects=True)
                resp.raise_for_status()
                return resp.text
            except httpx.HTTPStatusError as e:
                # Retry on 5xx and 429
                if e.response.status_code >= 500 or e.response.status_code == 429:
                    if attempt < max_retries - 1:
                        wait = 2 ** attempt
                        await asyncio.sleep(wait)
                        continue
                raise
            except httpx.RequestError as e:
                # Network errors — retry
                if attempt < max_retries - 1:
                    wait = 2 ** attempt
                    await asyncio.sleep(wait)
                    continue
                raise
    raise RuntimeError(f"Failed to fetch {url} after {max_retries} attempts")
