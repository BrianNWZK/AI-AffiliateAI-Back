import logging
import random
import asyncio

logger = logging.getLogger("Ariel.CampaignManager")

class CampaignManager:
    def __init__(self):
        self.active_campaigns = []
        
    async def launch_or_optimize(self, opportunities, market_trends):
        """
        Launch affiliate/cpa/ecommerce/content campaigns based on ops and trends.
        Use GPT/AI to generate content, select offers, deploy creatives.
        Track performance and auto-optimize for ROI.
        """
        logger.info("CampaignManager: Launching/optimizing campaigns...")
        
        if not opportunities:
            logger.info("CampaignManager: No opportunities provided, skipping campaign launch")
            return
            
        # Process each opportunity
        for opp in opportunities[:3]:  # Limit to top 3 opportunities
            campaign = await self._create_campaign(opp, market_trends)
            self.active_campaigns.append(campaign)
            
        await asyncio.sleep(random.uniform(0.5, 2.0))
        logger.info(f"CampaignManager: {len(opportunities)} campaigns processed")
        
    async def _create_campaign(self, opportunity, market_trends):
        """Create a campaign based on opportunity and market trends"""
        campaign = {
            "id": f"camp_{random.randint(1000, 9999)}",
            "type": opportunity.get("type", "general"),
            "status": "active",
            "budget": random.uniform(100, 1000),
            "target_roi": random.uniform(2.0, 5.0),
            "created_at": asyncio.get_event_loop().time()
        }
        
        logger.info(f"CampaignManager: Created campaign {campaign['id']} for {campaign['type']}")
        return campaign
        
    async def get_active_campaigns(self):
        """Get list of active campaigns"""
        return [c for c in self.active_campaigns if c.get("status") == "active"]
