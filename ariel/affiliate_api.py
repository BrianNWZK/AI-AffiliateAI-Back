import logging
import asyncio
import random

logger = logging.getLogger("Ariel.AffiliateAPI")

class AffiliateAPI:
    def __init__(self):
        self.base_url = "https://api.example-affiliate.com"
        
    async def fetch_offers(self):
        """Fetch available affiliate offers"""
        logger.info("AffiliateAPI: Fetching offers...")
        await asyncio.sleep(random.uniform(0.3, 0.8))
        
        # Mock offers data
        offers = [
            {
                "id": "offer_001",
                "name": "Tech Product Promotion",
                "commission": 15.5,
                "category": "technology",
                "payout": 25.00
            },
            {
                "id": "offer_002", 
                "name": "Health & Wellness Campaign",
                "commission": 12.0,
                "category": "health",
                "payout": 18.50
            },
            {
                "id": "offer_003",
                "name": "Digital Services Bundle",
                "commission": 20.0,
                "category": "services", 
                "payout": 35.00
            }
        ]
        
        logger.info(f"AffiliateAPI: Retrieved {len(offers)} offers")
        return offers
