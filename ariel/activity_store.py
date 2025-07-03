import logging
import asyncio
from datetime import datetime

logger = logging.getLogger("Ariel.ActivityStore")

class ActivityStore:
    def __init__(self, dsn=None):
        self.dsn = dsn or "sqlite:///ariel.db"
        self.activities = []  # In-memory store for demo
        
    async def setup(self):
        """Initialize the activity store"""
        logger.info("ActivityStore: Setting up storage...")
        await asyncio.sleep(0.1)
        logger.info("ActivityStore: Setup complete.")
        
    async def log_activity(self, activity):
        """Log an activity to the store"""
        activity_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "data": activity
        }
        self.activities.append(activity_record)
        logger.info(f"ActivityStore: Logged activity: {activity.get('cycle_id', 'unknown')}")
        
    async def get_recent_activities(self, limit=10):
        """Get recent activities"""
        return self.activities[-limit:] if self.activities else []
