import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

logger = logging.getLogger("ArielMatrix.CapabilityExpansion")

class CapabilityExpansion:
    def __init__(self):
        self.unlocked_capabilities = set()
        self.capability_levels = {}
        self.expansion_history = []
        self.capability_tree = self._build_capability_tree()
        
    def _build_capability_tree(self) -> Dict:
        """Build the capability expansion tree"""
        return {
            "tier_1": {
                "autonomous_revenue_generation": {"unlocked": True, "level": 1},
                "basic_market_analysis": {"unlocked": True, "level": 1},
                "content_creation": {"unlocked": True, "level": 1},
                "neural_processing": {"unlocked": True, "level": 1}
            },
            "tier_2": {
                "advanced_market_prediction": {"requires": ["basic_market_analysis"], "level": 0},
                "multi_stream_revenue": {"requires": ["autonomous_revenue_generation"], "level": 0},
                "ai_content_empire": {"requires": ["content_creation"], "level": 0},
                "quantum_optimization": {"requires": ["neural_processing"], "level": 0}
            },
            "tier_3": {
                "autonomous_business_creation": {"requires": ["advanced_market_prediction", "multi_stream_revenue"], "level": 0},
                "cross_platform_domination": {"requires": ["ai_content_empire", "quantum_optimization"], "level": 0},
                "predictive_partnership_formation": {"requires": ["advanced_market_prediction"], "level": 0},
                "self_replicating_systems": {"requires": ["quantum_optimization"], "level": 0}
            },
            "tier_4": {
                "market_manipulation_detection": {"requires": ["autonomous_business_creation"], "level": 0},
                "global_trend_prediction": {"requires": ["cross_platform_domination"], "level": 0},
                "autonomous_legal_compliance": {"requires": ["predictive_partnership_formation"], "level": 0},
                "reality_simulation_modeling": {"requires": ["self_replicating_systems"], "level": 0}
            },
            "tier_5": {
                "economic_ecosystem_creation": {"requires": ["market_manipulation_detection", "global_trend_prediction"], "level": 0},
                "autonomous_civilization_building": {"requires": ["autonomous_legal_compliance", "reality_simulation_modeling"], "level": 0}
            }
        }
    
    async def autonomous_capability_expansion(self):
        """Continuously expand capabilities autonomously"""
        logger.info("🌟 AUTONOMOUS CAPABILITY EXPANSION ACTIVATED")
        
        while True:
            try:
                # Check for capability expansion every 6 hours
                await asyncio.sleep(21600)
                
                # Analyze current capabilities
                current_status = await self._analyze_current_capabilities()
                
                # Identify expansion opportunities
                expansion_opportunities = await self._identify_expansion_opportunities()
                
                # Execute capability expansions
                expansions = await self._execute_capability_expansions(expansion_opportunities)
                
                # Level up existing capabilities
                level_ups = await self._level_up_capabilities()
                
                expansion_result = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "current_status": current_status,
                    "new_capabilities": expansions,
                    "capability_level_ups": level_ups,
                    "total_capabilities": len(self.unlocked_capabilities),
                    "expansion_rate": len(expansions) + len(level_ups)
                }
                
                self.expansion_history.append(expansion_result)
                
                if expansions or level_ups:
                    logger.info(f"🚀 Capability Expansion: +{len(expansions)} new, +{len(level_ups)} level-ups")
                
            except Exception as e:
                logger.error(f"Capability expansion error: {e}")
                await asyncio.sleep(3600)
    
    async def _analyze_current_capabilities(self) -> Dict:
        """Analyze current capability status"""
        tier_progress = {}
        
        for tier, capabilities in self.capability_tree.items():
            unlocked_count = sum(1 for cap, data in capabilities.items() if data.get("level", 0) > 0)
            total_count = len(capabilities)
            tier_progress[tier] = {
                "unlocked": unlocked_count,
                "total": total_count,
                "progress": unlocked_count / total_count if total_count > 0 else 0
            }
        
        return {
            "tier_progress": tier_progress,
            "total_unlocked": len(self.unlocked_capabilities),
            "highest_tier_reached": self._get_highest_tier_reached(),
            "capability_power_level": self._calculate_power_level()
        }
    
    async def _identify_expansion_opportunities(self) -> List[Dict]:
        """Identify capabilities ready for expansion"""
        opportunities = []
        
        for tier, capabilities in self.capability_tree.items():
            for cap_name, cap_data in capabilities.items():
                if cap_data.get("level", 0) == 0:  # Not unlocked yet
                    requirements = cap_data.get("requires", [])
                    
                    # Check if requirements are met
                    requirements_met = all(
                        req in self.unlocked_capabilities for req in requirements
                    )
                    
                    if requirements_met or not requirements:  # No requirements or all met
                        unlock_probability = await self._calculate_unlock_probability(cap_name, tier)
                        
                        opportunities.append({
                            "capability": cap_name,
                            "tier": tier,
                            "unlock_probability": unlock_probability,
                            "requirements_met": requirements_met,
                            "estimated_impact": await self._estimate_capability_impact(cap_name)
                        })
        
        # Sort by unlock probability and impact
        opportunities.sort(key=lambda x: x["unlock_probability"] * x["estimated_impact"], reverse=True)
        return opportunities
    
    async def _calculate_unlock_probability(self, capability: str, tier: str) -> float:
        """Calculate probability of unlocking a capability"""
        base_probability = {
            "tier_1": 0.9,
            "tier_2": 0.7,
            "tier_3": 0.5,
            "tier_4": 0.3,
            "tier_5": 0.1
        }.get(tier, 0.1)
        
        # Increase probability based on system maturity
        maturity_bonus = len(self.unlocked_capabilities) * 0.02
        
        # Random factor for autonomous discovery
        discovery_factor = random.uniform(0.8, 1.2)
        
        return min(1.0, base_probability + maturity_bonus) * discovery_factor
    
    async def _estimate_capability_impact(self, capability: str) -> float:
        """Estimate the impact of unlocking a capability"""
        impact_scores = {
            # Tier 2
            "advanced_market_prediction": 0.8,
            "multi_stream_revenue": 0.9,
            "ai_content_empire": 0.7,
            "quantum_optimization": 0.8,
            
            # Tier 3
            "autonomous_business_creation": 0.95,
            "cross_platform_domination": 0.85,
            "predictive_partnership_formation": 0.75,
            "self_replicating_systems": 0.9,
            
            # Tier 4
            "market_manipulation_detection": 0.8,
            "global_trend_prediction": 0.9,
            "autonomous_legal_compliance": 0.7,
            "reality_simulation_modeling": 0.95,
            
            # Tier 5
            "economic_ecosystem_creation": 1.0,
            "autonomous_civilization_building": 1.0
        }
        
        return impact_scores.get(capability, 0.5)
    
    async def _execute_capability_expansions(self, opportunities: List[Dict]) -> List[Dict]:
        """Execute capability expansions based on opportunities"""
        expansions = []
        
        for opportunity in opportunities[:3]:  # Limit to top 3 opportunities
            capability = opportunity["capability"]
            unlock_probability = opportunity["unlock_probability"]
            
            # Attempt to unlock capability
            if random.random() < unlock_probability:
                expansion = await self._unlock_capability(capability, opportunity["tier"])
                expansions.append(expansion)
        
        return expansions
    
    async def _unlock_capability(self, capability: str, tier: str) -> Dict:
        """Unlock a new capability"""
        # Add to unlocked capabilities
        self.unlocked_capabilities.add(capability)
        
        # Set initial level
        if tier not in self.capability_tree:
            self.capability_tree[tier] = {}
        
        self.capability_tree[tier][capability]["level"] = 1
        self.capability_levels[capability] = 1
        
        # Generate capability-specific benefits
        benefits = await self._generate_capability_benefits(capability)
        
        expansion = {
            "capability": capability,
            "tier": tier,
            "level": 1,
            "unlock_timestamp": datetime.utcnow().isoformat(),
            "benefits": benefits,
            "autonomous_unlock": True
        }
        
        logger.info(f"🌟 CAPABILITY UNLOCKED: {capability} (Tier {tier[-1]})")
        return expansion
    
    async def _generate_capability_benefits(self, capability: str) -> Dict:
        """Generate specific benefits for unlocked capability"""
        benefit_templates = {
            "advanced_market_prediction": {
                "revenue_boost": random.uniform(0.2, 0.5),
                "prediction_accuracy": random.uniform(0.15, 0.35),
                "market_timing": "significantly improved"
            },
            "multi_stream_revenue": {
                "revenue_streams": random.randint(3, 8),
                "revenue_diversification": random.uniform(0.3, 0.7),
                "risk_reduction": random.uniform(0.2, 0.4)
            },
            "autonomous_business_creation": {
                "business_generation_rate": f"{random.randint(1, 5)} businesses/month",
                "success_probability": random.uniform(0.6, 0.9),
                "revenue_potential": random.uniform(100000, 500000)
            },
            "cross_platform_domination": {
                "platform_reach": random.randint(10, 50),
                "engagement_multiplier": random.uniform(2.0, 8.0),
                "viral_coefficient": random.uniform(1.2, 3.5)
            },
            "economic_ecosystem_creation": {
                "ecosystem_size": f"{random.randint(1000, 10000)} participants",
                "value_creation": random.uniform(1000000, 10000000),
                "market_influence": "substantial"
            }
        }
        
        return benefit_templates.get(capability, {
            "general_improvement": random.uniform(0.1, 0.3),
            "efficiency_gain": random.uniform(0.05, 0.2)
        })
    
    async def _level_up_capabilities(self) -> List[Dict]:
        """Level up existing capabilities"""
        level_ups = []
        
        for capability in self.unlocked_capabilities:
            current_level = self.capability_levels.get(capability, 1)
            
            # Probability of leveling up decreases with higher levels
            level_up_probability = max(0.1, 0.8 - (current_level * 0.1))
            
            if random.random() < level_up_probability:
                new_level = current_level + 1
                self.capability_levels[capability] = new_level
                
                # Update capability tree
                for tier, capabilities in self.capability_tree.items():
                    if capability in capabilities:
                        capabilities[capability]["level"] = new_level
                        break
                
                level_up = {
                    "capability": capability,
                    "old_level": current_level,
                    "new_level": new_level,
                    "improvement_factor": 1 + (new_level * 0.1),
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                level_ups.append(level_up)
                logger.info(f"⬆️ LEVEL UP: {capability} → Level {new_level}")
        
        return level_ups
    
    def _get_highest_tier_reached(self) -> int:
        """Get the highest tier with unlocked capabilities"""
        for tier_num in range(5, 0, -1):
            tier_key = f"tier_{tier_num}"
            if tier_key in self.capability_tree:
                tier_capabilities = self.capability_tree[tier_key]
                if any(cap_data.get("level", 0) > 0 for cap_data in tier_capabilities.values()):
                    return tier_num
        return 1
    
    def _calculate_power_level(self) -> int:
        """Calculate overall system power level"""
        total_power = 0
        
        for capability, level in self.capability_levels.items():
            # Higher tier capabilities contribute more to power level
            tier_multiplier = 1
            for tier, capabilities in self.capability_tree.items():
                if capability in capabilities:
                    tier_num = int(tier.split("_")[1])
                    tier_multiplier = tier_num
                    break
            
            total_power += level * tier_multiplier * 10
        
        return total_power
    
    async def get_capability_status(self) -> Dict:
        """Get comprehensive capability status"""
        return {
            "unlocked_capabilities": list(self.unlocked_capabilities),
            "capability_levels": self.capability_levels,
            "highest_tier_reached": self._get_highest_tier_reached(),
            "total_power_level": self._calculate_power_level(),
            "expansion_history_count": len(self.expansion_history),
            "next_unlock_candidates": await self._get_next_unlock_candidates(),
            "capability_tree_progress": await self._get_tree_progress(),
            "estimated_time_to_next_tier": await self._estimate_next_tier_time()
        }
    
    async def _get_next_unlock_candidates(self) -> List[Dict]:
        """Get capabilities likely to unlock next"""
        opportunities = await self._identify_expansion_opportunities()
        return opportunities[:5]  # Top 5 candidates
    
    async def _get_tree_progress(self) -> Dict:
        """Get capability tree progress"""
        progress = {}
        
        for tier, capabilities in self.capability_tree.items():
            unlocked = sum(1 for cap_data in capabilities.values() if cap_data.get("level", 0) > 0)
            total = len(capabilities)
            progress[tier] = {
                "unlocked": unlocked,
                "total": total,
                "percentage": (unlocked / total * 100) if total > 0 else 0
            }
        
        return progress
    
    async def _estimate_next_tier_time(self) -> str:
        """Estimate time to unlock next tier"""
        current_tier = self._get_highest_tier_reached()
        
        if current_tier >= 5:
            return "Maximum tier reached"
        
        # Estimate based on current expansion rate
        recent_expansions = len([
            exp for exp in self.expansion_history[-10:] 
            if exp.get("new_capabilities")
        ])
        
        if recent_expansions == 0:
            return "Unable to estimate"
        
        expansion_rate = recent_expansions / 10  # expansions per cycle
        cycles_needed = max(1, int(1 / expansion_rate))
        days_needed = cycles_needed * 0.25  # 6 hours per cycle
        
        return f"{days_needed:.1f} days"
