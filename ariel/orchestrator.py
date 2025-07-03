"""
Ariel Orchestrator: Main coordination system for autonomous, real revenue generation.
Coordinates all ArielMatrix components for maximum real revenue production, scaling across any domain: crypto, goods, services, entertainment, social media, and beyond.
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from decimal import Decimal
import sys
import os

# Add path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ariel.ariel import ArielMatrix
from database import get_db

logger = logging.getLogger("ArielOrchestrator")

class ArielOrchestrator:
    """
    Main orchestrator for the Ariel revenue generation system.
    Coordinates all components to maximize real, scalable, and diversified revenue production.
    """

    def __init__(self):
        self.matrix = ArielMatrix(orchestrator=self)
        self.running = False
        self.paused = False
        self.initialized = False

        # Performance tracking
        self.total_cycles = 0
        self.total_revenue = Decimal('0.00')
        self.cycle_time = 1800  # 30 minutes default
        self.last_cycle_duration = 0.0
        self.last_opportunities_found = 0

        # Revenue targets
        self.daily_target = Decimal('5000.00')  # Minimum $5000/day, scales automatically
        self.monthly_target = Decimal('150000.00')  # Minimum $150K/month, scales automatically

        # System state
        self.start_time = None
        self.last_revenue_check = None
        self.opportunities_cache = []
        self.trends_cache = {}

        # Database connection
        self.db = None

    async def bootstrap(self):
        """Initialize the orchestrator system."""
        logger.info("🚀 ArielOrchestrator Bootstrap: Initializing real revenue generation system...")

        try:
            # Initialize database connection
            self.db = await get_db()
            logger.info("✅ Database connection established")

            # Initialize ArielMatrix
            await self.matrix.bootstrap()
            logger.info("✅ ArielMatrix initialized")

            # Initialize dashboard metrics
            await self._initialize_dashboard_metrics()
            logger.info("✅ Dashboard metrics initialized")

            # Log bootstrap completion
            await self._log_activity("orchestrator_bootstrap_completed", {
                "total_components": 20,
                "revenue_streams": 7,
                "initial_daily_target": float(self.daily_target)
            })

            self.initialized = True
            self.start_time = datetime.utcnow()

            logger.info("🎉 ArielOrchestrator Bootstrap: System ready for real revenue generation!")

        except Exception as e:
            logger.error(f"ArielOrchestrator Bootstrap failed: {e}")
            raise

    async def _initialize_dashboard_metrics(self):
        """Initialize dashboard metrics in database."""
        try:
            existing_metrics = await self.db.find_one("dashboard_metrics")
            if not existing_metrics:
                initial_metrics = {
                    "initialized": True,
                    "timestamp": datetime.utcnow().isoformat(),
                    "total_cycles": 0,
                    "total_revenue": 0.0,
                    "last_cycle_duration": 0.0,
                    "last_opportunities": 0,
                    "last_updated": datetime.utcnow().isoformat()
                }
                await self.db.insert_one("dashboard_metrics", initial_metrics)
                logger.info("✅ Dashboard metrics initialized")
            else:
                logger.info("✅ Dashboard metrics already exist")
        except Exception as e:
            logger.error(f"Dashboard metrics initialization failed: {e}")

    async def run_cycle(self):
        """Run a single orchestrator cycle producing only real revenue."""
        if not self.initialized:
            await self.bootstrap()

        cycle_start_time = time.time()
        logger.info(f"🔄 Starting Orchestrator Cycle #{self.total_cycles + 1}")

        try:
            # Step 1: Find real opportunities (across all domains)
            logger.info("🔍 Finding revenue opportunities...")
            opportunities = await self.matrix.find_opportunities()
            self.opportunities_cache = opportunities
            self.last_opportunities_found = len(opportunities)

            # Step 2: Analyze trends
            logger.info("📈 Analyzing market trends...")
            trends = await self.matrix.analyze_trends()
            self.trends_cache = trends

            # Step 3: Acquire assets for opportunities
            logger.info("💼 Acquiring assets for opportunities...")
            await self.matrix.acquire_assets_for_opportunities(opportunities, trends)

            # Step 4: Launch or optimize campaigns
            logger.info("🚀 Launching/optimizing campaigns...")
            await self.matrix.launch_or_optimize(opportunities, trends)

            # Step 5: Generate revenue (real API calls/transactions only)
            logger.info("💰 Generating real revenue...")
            revenue_results = await self.matrix.generate_revenue()

            if revenue_results:
                cycle_revenue = Decimal(str(revenue_results.get("total_revenue", 0)))
                self.total_revenue += cycle_revenue
                logger.info(f"💎 Cycle Revenue: ${cycle_revenue:,.2f}")
                logger.info(f"💰 Total Revenue: ${self.total_revenue:,.2f}")

                # Dynamically scale the daily/monthly targets as revenue increases
                if self.total_revenue > self.monthly_target:
                    self.daily_target = max(self.daily_target, self.total_revenue / max(1, self.total_cycles) * 1.1)
                    self.monthly_target = max(self.monthly_target, self.total_revenue * 1.05)

            # Step 6: Ensure minimum assets
            logger.info("🔧 Ensuring minimum assets...")
            await self.matrix.ensure_minimum_assets()

            # Step 7: Run autonomous experiments
            logger.info("🧪 Running autonomous experiments...")
            await self.matrix.autonomous_experimentation(opportunities, trends)

            # Step 8: Process system revenue events
            logger.info("⚡ Processing system revenue events...")
            await self.matrix.system_revenue_event(opportunities, trends)

            # Update cycle metrics
            cycle_end_time = time.time()
            self.last_cycle_duration = cycle_end_time - cycle_start_time
            self.total_cycles += 1

            # Log cycle completion
            await self._log_cycle_completion(revenue_results)
            await self._update_dashboard_metrics()

            logger.info(f"✅ Cycle #{self.total_cycles} completed in {self.last_cycle_duration:.2f}s")

        except Exception as e:
            logger.error(f"Orchestrator cycle failed: {e}")
            raise

    async def run_forever(self):
        """Run the orchestrator continuously, scaling into all revenue domains."""
        logger.info("🚀 Starting continuous real revenue generation...")

        self.running = True

        while self.running:
            try:
                if not self.paused:
                    await self.run_cycle()
                    logger.info(f"⏰ Waiting {self.cycle_time}s until next cycle...")
                    await asyncio.sleep(self.cycle_time)
                else:
                    logger.info("⏸️ System paused, waiting...")
                    await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Orchestrator error: {e}")
                await asyncio.sleep(300)

    def stop(self):
        """Stop the orchestrator."""
        logger.info("🛑 Stopping orchestrator...")
        self.running = False

    def pause(self):
        """Pause the orchestrator."""
        logger.info("⏸️ Pausing orchestrator...")
        self.paused = True

    def resume(self):
        """Resume the orchestrator."""
        logger.info("▶️ Resuming orchestrator...")
        self.paused = False

    async def _log_activity(self, activity: str, data: Dict = None):
        """Log orchestrator activity."""
        try:
            log_entry = {
                "activity": activity,
                "timestamp": datetime.utcnow().isoformat(),
                "cycle_number": self.total_cycles,
                "total_revenue": float(self.total_revenue),
                "data": data or {}
            }
            await self.db.insert_one("ariel_logs", log_entry)
        except Exception as e:
            logger.error(f"Activity logging failed: {e}")

    async def _log_cycle_completion(self, revenue_results: Dict):
        """Log cycle completion details."""
        try:
            cycle_data = {
                "cycle_number": self.total_cycles + 1,
                "duration": self.last_cycle_duration,
                "opportunities_found": self.last_opportunities_found,
                "revenue_generated": revenue_results.get("total_revenue", 0) if revenue_results else 0,
                "timestamp": datetime.utcnow().isoformat()
            }
            await self.db.insert_one("cycle_history", cycle_data)
            await self._log_activity("cycle_completed", {
                "cycle_number": self.total_cycles + 1,
                "duration": self.last_cycle_duration,
                "opportunities": self.last_opportunities_found,
                "revenue": revenue_results.get("total_revenue", 0) if revenue_results else 0
            })
        except Exception as e:
            logger.error(f"Cycle logging failed: {e}")

    async def _update_dashboard_metrics(self):
        """Update dashboard metrics."""
        try:
            await self.db.delete_many("dashboard_metrics", {})
            updated_metrics = {
                "initialized": True,
                "timestamp": datetime.utcnow().isoformat(),
                "total_cycles": self.total_cycles,
                "total_revenue": float(self.total_revenue),
                "last_cycle_duration": self.last_cycle_duration,
                "last_opportunities": self.last_opportunities_found,
                "last_updated": datetime.utcnow().isoformat()
            }
            await self.db.insert_one("dashboard_metrics", updated_metrics)
        except Exception as e:
            logger.error(f"Dashboard metrics update failed: {e}")

    async def get_status(self) -> Dict:
        """Get comprehensive orchestrator status."""
        try:
            matrix_status = await self.matrix.get_status()
            uptime = (datetime.utcnow() - self.start_time).total_seconds() if self.start_time else 0
            avg_cycle_duration = self.last_cycle_duration
            daily_revenue_rate = float(self.total_revenue) / max(1, uptime / 86400) if uptime > 0 else 0
            daily_progress = (daily_revenue_rate / float(self.daily_target)) * 100

            status = {
                "orchestrator": {
                    "initialized": self.initialized,
                    "running": self.running,
                    "paused": self.paused,
                    "total_cycles": self.total_cycles,
                    "uptime_seconds": uptime,
                    "last_cycle_duration": self.last_cycle_duration,
                    "cycle_time": self.cycle_time
                },
                "revenue": {
                    "total_revenue": float(self.total_revenue),
                    "daily_target": float(self.daily_target),
                    "monthly_target": float(self.monthly_target),
                    "daily_revenue_rate": daily_revenue_rate,
                    "daily_progress_percent": daily_progress
                },
                "performance": {
                    "last_opportunities_found": self.last_opportunities_found,
                    "avg_cycle_duration": avg_cycle_duration,
                    "opportunities_cached": len(self.opportunities_cache),
                    "trends_cached": len(self.trends_cache)
                },
                "matrix_status": matrix_status,
                "timestamp": datetime.utcnow().isoformat()
            }

            return status

        except Exception as e:
            logger.error(f"Status check failed: {e}")
            return {"error": str(e), "initialized": self.initialized}

    async def get_revenue_summary(self) -> Dict:
        """Get detailed revenue summary."""
        try:
            real_revenue_summary = await self.matrix.get_real_revenue_summary()
            uptime_days = (datetime.utcnow() - self.start_time).days if self.start_time else 0
            avg_daily_revenue = float(self.total_revenue) / max(1, uptime_days)
            return {
                "orchestrator_revenue": {
                    "total_revenue": float(self.total_revenue),
                    "uptime_days": uptime_days,
                    "avg_daily_revenue": avg_daily_revenue,
                    "total_cycles": self.total_cycles,
                    "revenue_per_cycle": float(self.total_revenue) / max(1, self.total_cycles)
                },
                "real_revenue_summary": real_revenue_summary,
                "projections": {
                    "projected_monthly": avg_daily_revenue * 30,
                    "projected_yearly": avg_daily_revenue * 365
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Revenue summary failed: {e}")
            return {"error": str(e)}

    async def get_dashboard_data(self) -> Dict:
        """Get data for dashboard display."""
        try:
            dashboard_metrics = await self.db.find_one("dashboard_metrics")
            cycle_history = await self.db.to_list("cycle_history", 10)
            recent_logs = await self.db.to_list("ariel_logs", 20)
            current_status = await self.get_status()
            return {
                "dashboard_metrics": dashboard_metrics,
                "cycle_history": cycle_history,
                "recent_logs": recent_logs,
                "current_status": current_status,
                "last_updated": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Dashboard data retrieval failed: {e}")
            return {"error": str(e)}

    # Properties for easy access
    @property
    def quantum(self):
        return self.matrix.quantum_research

    @property
    def neural(self):
        return self.matrix.neural_engine

    @property
    def campaign_manager(self):
        return self.matrix.campaign_manager
