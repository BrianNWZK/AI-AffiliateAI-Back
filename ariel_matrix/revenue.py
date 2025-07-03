from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ariel_matrix.ariel_user import ARIEL

class Revenue(BaseModel):
    revenue_id: str
    user_id: str = ARIEL.user_id
    amount: float
    currency: str = "USD"
    timestamp: str = datetime.utcnow().isoformat()
    source: str = "autonomous_system"
    signature: str
    metadata: Optional[dict] = None

class RevenueTracker:
    def __init__(self):
        self.revenue_records = []
        self.total_revenue = 0.0

    async def record_revenue(self, revenue: Revenue):
        # Cryptographically sign every revenue event
        message = f"{revenue.revenue_id}:{revenue.amount}:{revenue.currency}:{revenue.timestamp}".encode("utf-8")
        revenue.signature = ARIEL.sign_message(message)
        self.revenue_records.append(revenue)
        self.total_revenue += revenue.amount
