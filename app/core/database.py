import os
from typing import Optional
from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables from a .env file (if present)
load_dotenv()

# Environment-configurable MongoDB URI and database name
MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB: str = os.getenv("MONGODB_DB", "ecom_db")

# We intentionally create the client in application startup to avoid connecting at import time.
client: Optional[AsyncIOMotorClient] = None


async def connect_to_mongo(app) -> None:
    """Create Motor client and attach DB to the FastAPI app state.

    Usage: call this in a FastAPI startup event handler.
    """
    global client
    client = AsyncIOMotorClient(MONGODB_URI)
    app.state.mongodb_client = client
    app.state.mongodb = client[MONGODB_DB]

    # Optional lightweight ping to verify connection; logs if needed.
    try:
        await app.state.mongodb.command("ping")
        print("Connected to MongoDB")
    except Exception as exc:  # pragma: no cover - connectivity depends on environment
        print("Failed to connect to MongoDB:", exc)
        raise


async def close_mongo_connection(app) -> None:
    """Close Motor client. Call this in a FastAPI shutdown event handler."""
    global client
    if client is not None:
        client.close()


def get_database(request) -> Optional[object]:
    """FastAPI dependency to get the Motor database instance from the app state.

    Example usage in a route: `db = Depends(get_database)`
    """
    return getattr(request.app.state, "mongodb", None)
