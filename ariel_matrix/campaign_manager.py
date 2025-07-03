import logging
import random
from datetime import datetime
from typing import Dict, List, Optional
from ariel_matrix.ariel_user import ARIEL

logger = logging.getLogger("ArielMatrix.CampaignManager")

class CampaignManager:
    def __init__(self):
        self.campaigns = []
        self.campaign_types = ['affiliate', 'social_media', 'content', 'email', 'ppc']
        self.active_campaigns = []

    async def launch_campaigns(self, opportunities: Optional[List[Dict]] = None):
        logger.info("Launching marketing campaigns...")
        if opportunities is None:
            opportunities = await self._generate_sample_opportunities()
        campaigns_launched = []
        for opportunity in opportunities[:5]:
            campaign = await self._create_campaign_from_opportunity(opportunity)
            campaign['campaign_id'] = ARIEL._generate_user_id()
            campaign['api_key'] = ARIEL._generate_api_key()
            campaign['signed_by'] = ARIEL.user_id
            self.campaigns.append(campaign)
            self.active_campaigns.append(campaign)
            campaigns_launched.append(campaign)
        return {
            "campaigns_launched": campaigns_launched,
            "bot_delegation": [ARIEL.create_bot(f"CampaignBot-{i}") for i in range(len(campaigns_launched))]
        }

    async def _generate_sample_opportunities(self):
        return [{"type": "affiliate_offer", "title": "Tech Products Campaign", "value_score": 85}]

    async def _create_campaign_from_opportunity(self, opportunity: Dict):
        return {
            "id": ARIEL._generate_user_id(),
            "type": opportunity.get('type', 'affiliate'),
            "title": opportunity.get('title', 'Untitled'),
            "budget": random.uniform(100, 1000),
            "created_at": datetime.utcnow().isoformat()
        }
