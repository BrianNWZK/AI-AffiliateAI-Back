import logging
import asyncio

logger = logging.getLogger("Ariel.AdminDashboard")

class AdminDashboard:
    def __init__(self):
        self.status_history = []
        self.activities = []
        
    async def setup(self):
        """Initialize dashboard components"""
        logger.info("AdminDashboard: Setting up dashboard...")
        await asyncio.sleep(0.1)
        logger.info("AdminDashboard: Dashboard ready.")

    async def sync_status(self, status_dict):
        """
        Push Ariel's status, logs, and AI activity to frontend dashboard.
        """
        self.status_history.append(status_dict)
        # Keep only last 100 status updates
        if len(self.status_history) > 100:
            self.status_history = self.status_history[-100:]
            
        logger.info(f"AdminDashboard: Status synced - Cycle {status_dict.get('cycle_id', 'unknown')}")

    async def push_activity(self, activity: dict):
        """
        Push a new Ariel activity event to the dashboard feed.
        """
        activity_with_timestamp = {
            **activity,
            "timestamp": asyncio.get_event_loop().time()
        }
        self.activities.append(activity_with_timestamp)
        
        # Keep only last 50 activities
        if len(self.activities) > 50:
            self.activities = self.activities[-50:]
            
        logger.info(f"AdminDashboard: Activity pushed: {activity.get('type', 'unknown')}")

    async def get_recent_activities(self, limit: int = 10):
        """
        Fetch most recent Ariel activities for dashboard display.
        """
        logger.info(f"AdminDashboard: Fetching {limit} recent activities")
        return self.activities[-limit:] if self.activities else []
        
    async def get_current_status(self):
        """Get the most recent status"""
        return self.status_history[-1] if self.status_history else None
