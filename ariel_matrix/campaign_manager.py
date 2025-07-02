import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

logger = logging.getLogger("ArielMatrix.CampaignManager")

class CampaignManager:
    def __init__(self):
        self.campaigns = []
        self.campaign_types = ['affiliate', 'social_media', 'content', 'email', 'ppc']
        self.active_campaigns = []
        
    async def launch_campaigns(self, opportunities: Optional[List[Dict]] = None):
        """Launch marketing campaigns based on opportunities"""
        logger.info("Launching marketing campaigns...")
        
        try:
            if opportunities is None:
                opportunities = await self._generate_sample_opportunities()
            
            campaigns_launched = []
            total_budget_allocated = 0
            expected_roi = 0
            
            for opportunity in opportunities[:5]:  # Limit to top 5 opportunities
                campaign = await self._create_campaign_from_opportunity(opportunity)
                self.campaigns.append(campaign)
                self.active_campaigns.append(campaign)
                campaigns_launched.append(campaign)
                
                total_budget_allocated += campaign.get('budget', 0)
                expected_roi += campaign.get('expected_revenue', 0)
            
            # Optimize existing campaigns
            optimization_results = await self._optimize_existing_campaigns()
            
            launch_result = {
                "timestamp": datetime.utcnow().isoformat(),
                "campaigns_launched": campaigns_launched,
                "total_budget_allocated": total_budget_allocated,
                "expected_roi": expected_roi,
                "optimization_results": optimization_results,
                "campaign_summary": await self.get_campaign_summary()
            }
            
            logger.info(f"Campaign launch completed. {len(campaigns_launched)} campaigns launched")
            return launch_result
            
        except Exception as e:
            logger.error(f"Campaign launch failed: {e}")
            raise
    
    async def _generate_sample_opportunities(self):
        """Generate sample opportunities for campaign creation"""
        return [
            {
                "type": "affiliate_offer",
                "title": "Tech Products Campaign",
                "value_score": 85,
                "commission": 15.0,
                "target_audience": "tech_enthusiasts"
            },
            {
                "type": "social_media",
                "title": "Health & Wellness Content",
                "value_score": 78,
                "engagement_rate": 4.2,
                "target_audience": "health_conscious"
            },
            {
                "type": "email_marketing",
                "title": "Digital Services Promotion",
                "value_score": 72,
                "conversion_rate": 3.1,
                "target_audience": "small_business"
            }
        ]
    
    async def _create_campaign_from_opportunity(self, opportunity: Dict):
        """Create a campaign based on an opportunity"""
        await asyncio.sleep(0.1)  # Simulate campaign creation time
        
        campaign_id = f"campaign_{random.randint(10000, 99999)}"
        
        # Determine campaign type based on opportunity
        campaign_type = self._determine_campaign_type(opportunity)
        
        # Calculate budget and expected revenue
        budget = self._calculate_budget(opportunity)
        expected_revenue = budget * random.uniform(1.2, 3.5)  # ROI between 120% and 350%
        
        campaign = {
            "id": campaign_id,
            "type": campaign_type,
            "title": opportunity.get('title', f'Campaign {campaign_id}'),
            "opportunity_source": opportunity.get('type', 'unknown'),
            "budget": budget,
            "expected_revenue": expected_revenue,
            "target_audience": opportunity.get('target_audience', 'general'),
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "duration_days": random.randint(7, 30),
            "channels": self._select_channels(campaign_type),
            "kpis": self._generate_kpis(campaign_type),
            "value_score": opportunity.get('value_score', 50)
        }
        
        return campaign
    
    def _determine_campaign_type(self, opportunity: Dict):
        """Determine campaign type based on opportunity"""
        opp_type = opportunity.get('type', '')
        
        if 'affiliate' in opp_type:
            return 'affiliate'
        elif 'social' in opp_type:
            return 'social_media'
        elif 'email' in opp_type:
            return 'email'
        elif 'content' in opp_type:
            return 'content'
        else:
            return random.choice(self.campaign_types)
    
    def _calculate_budget(self, opportunity: Dict):
        """Calculate campaign budget based on opportunity value"""
        value_score = opportunity.get('value_score', 50)
        base_budget = 100  # Base budget in USD
        
        # Scale budget based on value score
        budget_multiplier = value_score / 50  # Normalize to 1.0 at score 50
        budget = base_budget * budget_multiplier
        
        # Add some randomness
        budget *= random.uniform(0.8, 1.5)
        
        return round(budget, 2)
    
    def _select_channels(self, campaign_type: str):
        """Select appropriate channels for campaign type"""
        channel_map = {
            'affiliate': ['affiliate_networks', 'email', 'social_media'],
            'social_media': ['facebook', 'instagram', 'twitter', 'linkedin'],
            'content': ['blog', 'youtube', 'podcast', 'social_media'],
            'email': ['email_campaigns', 'newsletters', 'automation'],
            'ppc': ['google_ads', 'facebook_ads', 'bing_ads']
        }
        
        available_channels = channel_map.get(campaign_type, ['general'])
        return random.sample(available_channels, min(3, len(available_channels)))
    
    def _generate_kpis(self, campaign_type: str):
        """Generate KPIs for campaign type"""
        base_kpis = {
            'target_impressions': random.randint(10000, 100000),
            'target_clicks': random.randint(500, 5000),
            'target_conversions': random.randint(10, 200),
            'target_ctr': random.uniform(1.0, 5.0),
            'target_conversion_rate': random.uniform(1.0, 8.0)
        }
        
        # Add campaign-specific KPIs
        if campaign_type == 'affiliate':
            base_kpis['target_commission'] = random.uniform(500, 5000)
        elif campaign_type == 'social_media':
            base_kpis['target_engagement_rate'] = random.uniform(2.0, 8.0)
            base_kpis['target_followers'] = random.randint(100, 2000)
        elif campaign_type == 'email':
            base_kpis['target_open_rate'] = random.uniform(15.0, 35.0)
            base_kpis['target_click_rate'] = random.uniform(2.0, 8.0)
        
        return base_kpis
    
    async def _optimize_existing_campaigns(self):
        """Optimize existing active campaigns"""
        optimizations = []
        
        for campaign in self.active_campaigns:
            if random.random() > 0.6:  # 40% chance to optimize each campaign
                optimization = await self._optimize_campaign(campaign)
                optimizations.append(optimization)
        
        return optimizations
    
    async def _optimize_campaign(self, campaign: Dict):
        """Optimize a specific campaign"""
        await asyncio.sleep(0.1)  # Simulate optimization time
        
        optimization_types = ['budget_reallocation', 'audience_refinement', 'creative_update', 'channel_optimization']
        optimization_type = random.choice(optimization_types)
        
        # Simulate optimization impact
        impact = random.uniform(5, 25)  # 5-25% improvement
        
        optimization = {
            "campaign_id": campaign['id'],
            "optimization_type": optimization_type,
            "impact_percentage": impact,
            "timestamp": datetime.utcnow().isoformat(),
            "details": self._get_optimization_details(optimization_type, impact)
        }
        
        return optimization
    
    def _get_optimization_details(self, optimization_type: str, impact: float):
        """Get details for optimization type"""
        details_map = {
            'budget_reallocation': f"Reallocated budget to top-performing channels, expected {impact:.1f}% ROI improvement",
            'audience_refinement': f"Refined target audience based on performance data, expected {impact:.1f}% conversion improvement",
            'creative_update': f"Updated ad creatives and copy, expected {impact:.1f}% engagement improvement",
            'channel_optimization': f"Optimized channel mix and bidding, expected {impact:.1f}% cost efficiency improvement"
        }
        
        return details_map.get(optimization_type, f"Applied {optimization_type} optimization")
    
    async def get_active_campaigns(self):
        """Get list of active campaigns"""
        return [c for c in self.campaigns if c.get('status') == 'active']
    
    async def get_campaign_summary(self):
        """Get summary of all campaigns"""
        active_campaigns = await self.get_active_campaigns()
        
        summary = {
            "total_campaigns": len(self.campaigns),
            "active_campaigns": len(active_campaigns),
            "total_budget": sum(c.get('budget', 0) for c in active_campaigns),
            "expected_revenue": sum(c.get('expected_revenue', 0) for c in active_campaigns),
            "average_value_score": sum(c.get('value_score', 0) for c in active_campaigns) / max(len(active_campaigns), 1),
            "campaign_types": {
                campaign_type: len([c for c in active_campaigns if c.get('type') == campaign_type])
                for campaign_type in self.campaign_types
            }
        }
        
        return summary
    
    async def launch_or_optimize(self, opportunities: List[Dict], market_trends: Dict):
        """Launch new campaigns or optimize existing ones based on opportunities and trends"""
        logger.info("Launching or optimizing campaigns based on opportunities and market trends...")
        
        try:
            # Analyze market trends to adjust strategy
            strategy_adjustments = await self._analyze_trends_for_strategy(market_trends)
            
            # Launch new campaigns for high-value opportunities
            high_value_opportunities = [opp for opp in opportunities if opp.get('value_score', 0) > 75]
            
            if high_value_opportunities:
                launch_results = await self.launch_campaigns(high_value_opportunities)
            else:
                launch_results = {"campaigns_launched": [], "total_budget_allocated": 0}
            
            # Optimize existing campaigns based on trends
            optimization_results = await self._optimize_for_trends(strategy_adjustments)
            
            combined_results = {
                "action": "launch_or_optimize",
                "timestamp": datetime.utcnow().isoformat(),
                "launch_results": launch_results,
                "optimization_results": optimization_results,
                "strategy_adjustments": strategy_adjustments,
                "market_trend": market_trends.get('trend', 'stable')
            }
            
            return combined_results
            
        except Exception as e:
            logger.error(f"Campaign launch/optimization failed: {e}")
            raise
    
    async def _analyze_trends_for_strategy(self, market_trends: Dict):
        """Analyze market trends to determine strategy adjustments"""
        trend = market_trends.get('trend', 'stable')
        confidence = market_trends.get('confidence', 0.5)
        
        adjustments = {
            "budget_adjustment": 1.0,  # Multiplier for budget allocation
            "risk_tolerance": "medium",
            "channel_preference": [],
            "audience_focus": "broad"
        }
        
        if trend == 'bullish' and confidence > 0.7:
            adjustments.update({
                "budget_adjustment": 1.3,
                "risk_tolerance": "high",
                "channel_preference": ["social_media", "ppc"],
                "audience_focus": "growth_oriented"
            })
        elif trend == 'bearish' and confidence > 0.7:
            adjustments.update({
                "budget_adjustment": 0.7,
                "risk_tolerance": "low",
                "channel_preference": ["email", "content"],
                "audience_focus": "retention_focused"
            })
        
        return adjustments
    
    async def _optimize_for_trends(self, strategy_adjustments: Dict):
        """Optimize campaigns based on strategy adjustments"""
        optimizations = []
        
        budget_multiplier = strategy_adjustments.get('budget_adjustment', 1.0)
        preferred_channels = strategy_adjustments.get('channel_preference', [])
        
        for campaign in self.active_campaigns:
            # Adjust budget based on trend
            if budget_multiplier != 1.0:
                old_budget = campaign.get('budget', 0)
                new_budget = old_budget * budget_multiplier
                campaign['budget'] = new_budget
                
                optimizations.append({
                    "campaign_id": campaign['id'],
                    "optimization_type": "budget_adjustment",
                    "old_budget": old_budget,
                    "new_budget": new_budget,
                    "reason": f"Market trend adjustment ({strategy_adjustments.get('risk_tolerance', 'medium')} risk)"
                })
            
            # Optimize channels based on preferences
            if preferred_channels and campaign.get('channels'):
                campaign_channels = campaign['channels']
                if any(channel in preferred_channels for channel in campaign_channels):
                    optimizations.append({
                        "campaign_id": campaign['id'],
                        "optimization_type": "channel_prioritization",
                        "prioritized_channels": [ch for ch in campaign_channels if ch in preferred_channels],
                        "reason": "Market trend channel optimization"
                    })
        
        return optimizations
