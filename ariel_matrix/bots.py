import asyncio
import logging
import aiohttp
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger("ArielMatrix.BotManager")

class OpportunityBot:
    def __init__(self, target_site: str, aggregator, keywords: Optional[List[str]] = None):
        self.target_site = target_site
        self.aggregator = aggregator
        self.keywords = keywords or [
            "opportunity", "reward", "bounty", "contest", "grant", 
            "open call", "competition", "affiliate", "partnership",
            "revenue share", "commission", "referral", "cashback"
        ]
        self.findings = []

    async def run(self):
        """Run the opportunity bot to scan target site"""
        logger.info(f"OpportunityBot scanning: {self.target_site}")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    self.target_site, 
                    timeout=aiohttp.ClientTimeout(total=10),
                    headers={'User-Agent': 'Mozilla/5.0 (compatible; OpportunityBot/1.0)'}
                ) as resp:
                    if resp.status == 200:
                        html = await resp.text()
                        findings = await self._analyze_content(html)
                        
                        if findings:
                            self.aggregator.report({
                                "site": self.target_site,
                                "bot_type": "opportunity_scanner",
                                "findings": findings,
                                "scan_timestamp": datetime.utcnow().isoformat(),
                                "status": "success"
                            })
                            self.findings.extend(findings)
                            
                        return findings
                    else:
                        logger.warning(f"Bot failed to access {self.target_site}: HTTP {resp.status}")
                        return []
                        
            except asyncio.TimeoutError:
                logger.warning(f"Bot timeout accessing {self.target_site}")
                return []
            except Exception as e:
                logger.error(f"Bot error scanning {self.target_site}: {e}")
                return []

    async def _analyze_content(self, html: str):
        """Analyze HTML content for opportunities"""
        findings = []
        html_lower = html.lower()
        
        # Check for keyword matches
        matched_keywords = [kw for kw in self.keywords if kw in html_lower]
        
        if matched_keywords:
            # Simulate more detailed analysis
            await asyncio.sleep(0.1)
            
            finding = {
                "type": "keyword_match",
                "matched_keywords": matched_keywords,
                "keyword_count": len(matched_keywords),
                "confidence_score": min(100, len(matched_keywords) * 10),
                "content_length": len(html),
                "potential_value": self._estimate_value(matched_keywords, html)
            }
            findings.append(finding)
        
        # Look for specific patterns (simplified)
        patterns = {
            "email_signup": ["subscribe", "newsletter", "email"],
            "affiliate_links": ["affiliate", "partner", "commission"],
            "contact_forms": ["contact", "form", "submit"],
            "pricing_info": ["price", "$", "cost", "fee"]
        }
        
        for pattern_name, pattern_keywords in patterns.items():
            if any(keyword in html_lower for keyword in pattern_keywords):
                findings.append({
                    "type": "pattern_match",
                    "pattern": pattern_name,
                    "confidence_score": 70,
                    "description": f"Found {pattern_name} indicators on page"
                })
        
        return findings

    def _estimate_value(self, keywords: List[str], html: str):
        """Estimate potential value based on keywords and content"""
        base_value = len(keywords) * 10
        
        # Bonus for high-value keywords
        high_value_keywords = ["affiliate", "commission", "revenue", "partnership", "grant"]
        bonus = sum(20 for kw in keywords if kw in high_value_keywords)
        
        # Content length factor
        content_factor = min(50, len(html) // 1000)
        
        return base_value + bonus + content_factor

class BotManager:
    def __init__(self):
        self.active_bots = []
        self.bot_results = []
        self.default_targets = [
            "https://example-contests.com",
            "https://sample-grants.org", 
            "https://demo-affiliate-programs.com",
            "https://test-partnerships.net",
            "https://mock-opportunities.io"
        ]

    async def deploy_bots(self, targets: Optional[List[str]] = None, aggregator=None):
        """Deploy opportunity bots to scan multiple targets"""
        logger.info("Deploying opportunity bots...")
        
        if targets is None:
            targets = self.default_targets
        
        if aggregator is None:
            aggregator = self._create_default_aggregator()
        
        try:
            # Create and deploy bots
            bots = []
            for target in targets:
                bot = OpportunityBot(target, aggregator)
                bots.append(bot)
                self.active_bots.append(bot)
            
            # Run bots concurrently
            bot_tasks = [bot.run() for bot in bots]
            results = await asyncio.gather(*bot_tasks, return_exceptions=True)
            
            # Process results
            all_findings = []
            successful_scans = 0
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Bot failed for {targets[i]}: {result}")
                else:
                    all_findings.extend(result)
                    if result:
                        successful_scans += 1
            
            deployment_result = {
                "timestamp": datetime.utcnow().isoformat(),
                "bots_deployed": len(bots),
                "targets_scanned": len(targets),
                "successful_scans": successful_scans,
                "total_findings": len(all_findings),
                "findings": all_findings,
                "bot_summary": await self.get_bot_summary()
            }
            
            self.bot_results.append(deployment_result)
            
            logger.info(f"Bot deployment completed. {successful_scans}/{len(targets)} successful scans, {len(all_findings)} findings")
            return deployment_result
            
        except Exception as e:
            logger.error(f"Bot deployment failed: {e}")
            raise

    def _create_default_aggregator(self):
        """Create a default aggregator for bots"""
        class DefaultAggregator:
            def __init__(self):
                self.reports = []
            
            def report(self, data):
                self.reports.append(data)
        
        return DefaultAggregator()

    async def get_bot_summary(self):
        """Get summary of bot activities"""
        total_bots = len(self.active_bots)
        total_findings = sum(len(bot.findings) for bot in self.active_bots)
        
        summary = {
            "total_bots_deployed": total_bots,
            "total_findings": total_findings,
            "average_findings_per_bot": total_findings / max(total_bots, 1),
            "deployment_history": len(self.bot_results),
            "last_deployment": self.bot_results[-1]["timestamp"] if self.bot_results else None
        }
        
        return summary

    async def stop_all_bots(self):
        """Stop all active bots"""
        logger.info("Stopping all active bots...")
        self.active_bots.clear()
        logger.info("All bots stopped")

    async def get_bot_findings(self, limit: int = 50):
        """Get recent bot findings"""
        all_findings = []
        for bot in self.active_bots:
            all_findings.extend(bot.findings)
        
        # Sort by most recent and limit
        all_findings.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return all_findings[:limit]
