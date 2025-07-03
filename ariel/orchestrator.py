"""
Ariel Orchestrator: Main coordination system for autonomous revenue generation
Coordinates all ArielMatrix components for maximum revenue generation
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
    Main orchestrator for the Ariel revenue generation system
    Coordinates all components to maximize real revenue generation
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
        self.daily_target = Decimal('1000000.00')  # $1M daily target
        self.monthly_target = Decimal('30000000.00')  # $30M monthly target
        self.billionaire_target = Decimal('250000000000.00')  # $250B ultimate target
        
        # System state
        self.start_time = None
        self.last_revenue_check = None
        self.opportunities_cache = []
        self.trends_cache = {}
        
        # Database connection
        self.db = None
    
    async def bootstrap(self):
        """Initialize the complete orchestrator system"""
        logger.info("🚀 ArielOrchestrator Bootstrap: Initializing revenue generation system...")
        
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
                "target_revenue": float(self.billionaire_target)
            })
            
            self.initialized = True
            self.start_time = datetime.utcnow()
            
            logger.info("🎉 ArielOrchestrator Bootstrap: System ready for revenue generation!")
            
        except Exception as e:
            logger.error(f"ArielOrchestrator Bootstrap failed: {e}")
            raise
    
    async def _initialize_dashboard_metrics(self):
        """Initialize dashboard metrics in database"""
        try:
            # Check if metrics already exist
            existing_metrics = await self.db.find_one("dashboard_metrics")
            
            if not existing_metrics:
                # Create initial metrics
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
        """Run a single orchestrator cycle"""
        if not self.initialized:
            await self.bootstrap()
        
        cycle_start_time = time.time()
        logger.info(f"🔄 Starting Orchestrator Cycle #{self.total_cycles + 1}")
        
        try:
            # Step 1: Find opportunities
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
            
            # Step 5: Generate revenue
            logger.info("💰 Generating real revenue...")
            revenue_results = await self.matrix.generate_revenue()
            
            if revenue_results:
                cycle_revenue = Decimal(str(revenue_results.get("total_revenue", 0)))
                self.total_revenue += cycle_revenue
                
                logger.info(f"💎 Cycle Revenue: ${cycle_revenue:,.2f}")
                logger.info(f"💰 Total Revenue: ${self.total_revenue:,.2f}")
            
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
            
            # Update dashboard metrics
            await self._update_dashboard_metrics()
            
            # Check revenue milestones
            await self._check_revenue_milestones()
            
            logger.info(f"✅ Cycle #{self.total_cycles} completed in {self.last_cycle_duration:.2f}s")
            
        except Exception as e:
            logger.error(f"Orchestrator cycle failed: {e}")
            raise
    
    async def run_forever(self):
        """Run the orchestrator continuously"""
        logger.info("🚀 Starting continuous revenue generation...")
        
        self.running = True
        
        while self.running:
            try:
                if not self.paused:
                    await self.run_cycle()
                    
                    # Wait for next cycle
                    logger.info(f"⏰ Waiting {self.cycle_time}s until next cycle...")
                    await asyncio.sleep(self.cycle_time)
                else:
                    # System is paused
                    logger.info("⏸️ System paused, waiting...")
                    await asyncio.sleep(60)  # Check every minute
                    
            except Exception as e:
                logger.error(f"Orchestrator error: {e}")
                # Wait before retrying
                await asyncio.sleep(300)  # 5 minutes
    
    def stop(self):
        """Stop the orchestrator"""
        logger.info("🛑 Stopping orchestrator...")
        self.running = False
    
    def pause(self):
        """Pause the orchestrator"""
        logger.info("⏸️ Pausing orchestrator...")
        self.paused = True
    
    def resume(self):
        """Resume the orchestrator"""
        logger.info("▶️ Resuming orchestrator...")
        self.paused = False
    
    async def _log_activity(self, activity: str, data: Dict = None):
        """Log orchestrator activity"""
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
        """Log cycle completion details"""
        try:
            cycle_data = {
                "cycle_number": self.total_cycles + 1,
                "duration": self.last_cycle_duration,
                "opportunities_found": self.last_opportunities_found,
                "revenue_generated": revenue_results.get("total_revenue", 0) if revenue_results else 0,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await self.db.insert_one("cycle_history", cycle_data)
            
            # Also log as activity
            await self._log_activity("cycle_completed", {
                "cycle_number": self.total_cycles + 1,
                "duration": self.last_cycle_duration,
                "opportunities": self.last_opportunities_found,
                "revenue": revenue_results.get("total_revenue", 0) if revenue_results else 0
            })
            
        except Exception as e:
            logger.error(f"Cycle logging failed: {e}")
    
    async def _update_dashboard_metrics(self):
        """Update dashboard metrics"""
        try:
            # Delete old metrics
            await self.db.delete_many("dashboard_metrics", {})
            
            # Insert updated metrics
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
    
    async def _check_revenue_milestones(self):
        """Check and celebrate revenue milestones"""
        current_revenue = float(self.total_revenue)
        
        milestones = [
            (100000, "🎉 $100K MILESTONE ACHIEVED!"),
            (1000000, "🚀 MILLIONAIRE STATUS ACHIEVED!"),
            (10000000, "💎 $10M MILESTONE ACHIEVED!"),
            (100000000, "🌟 $100M MILESTONE ACHIEVED!"),
            (1000000000, "👑 BILLIONAIRE STATUS ACHIEVED!"),
            (10000000000, "🏆 $10B MILESTONE ACHIEVED!"),
            (100000000000, "🌍 $100B MILESTONE ACHIEVED!"),
            (250000000000, "🎯 TARGET ACHIEVED: SURPASSED ELON MUSK & JEFF BEZOS!")
        ]
        
        for milestone_amount, message in milestones:
            if current_revenue >= milestone_amount:
                logger.info(message)
                
                # Log milestone achievement
                await self._log_activity("milestone_achieved", {
                    "milestone_amount": milestone_amount,
                    "current_revenue": current_revenue,
                    "message": message
                })
                
                # Special handling for ultimate target
                if milestone_amount == 250000000000:
                    logger.info("🏆 CONGRATULATIONS! YOU ARE NOW RICHER THAN ELON MUSK AND JEFF BEZOS!")
                    logger.info("🌟 MISSION ACCOMPLISHED: $250 BILLION TARGET REACHED!")
    
    async def get_status(self) -> Dict:
        """Get comprehensive orchestrator status"""
        try:
            # Get ArielMatrix status
            matrix_status = await self.matrix.get_status()
            
            # Calculate performance metrics
            uptime = (datetime.utcnow() - self.start_time).total_seconds() if self.start_time else 0
            avg_cycle_duration = self.last_cycle_duration
            
            # Calculate revenue rates
            daily_revenue_rate = float(self.total_revenue) / max(1, uptime / 86400) if uptime > 0 else 0
            
            # Progress toward targets
            daily_progress = (daily_revenue_rate / float(self.daily_target)) * 100
            billionaire_progress = (float(self.total_revenue) / float(self.billionaire_target)) * 100
            
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
                    "billionaire_target": float(self.billionaire_target),
                    "daily_revenue_rate": daily_revenue_rate,
                    "daily_progress_percent": daily_progress,
                    "billionaire_progress_percent": billionaire_progress
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
        """Get detailed revenue summary"""
        try:
            # Get real revenue summary from ArielMatrix
            real_revenue_summary = await self.matrix.get_real_revenue_summary()
            
            # Get billionaire status
            billionaire_status = await self.matrix.get_billionaire_status()
            
            # Calculate additional metrics
            uptime_days = (datetime.utcnow() - self.start_time).days if self.start_time else 0
            avg_daily_revenue = float(self.total_revenue) / max(1, uptime_days)
            
            # Projection calculations
            days_to_billion = (1000000000 - float(self.total_revenue)) / max(avg_daily_revenue, 1000) if avg_daily_revenue > 0 else float('inf')
            days_to_target = (float(self.billionaire_target) - float(self.total_revenue)) / max(avg_daily_revenue, 1000) if avg_daily_revenue > 0 else float('inf')
            
            return {
                "orchestrator_revenue": {
                    "total_revenue": float(self.total_revenue),
                    "uptime_days": uptime_days,
                    "avg_daily_revenue": avg_daily_revenue,
                    "total_cycles": self.total_cycles,
                    "revenue_per_cycle": float(self.total_revenue) / max(1, self.total_cycles)
                },
                "real_revenue_summary": real_revenue_summary,
                "billionaire_status": billionaire_status,
                "projections": {
                    "days_to_billion": min(days_to_billion, 9999),
                    "days_to_target": min(days_to_target, 9999),
                    "projected_monthly": avg_daily_revenue * 30,
                    "projected_yearly": avg_daily_revenue * 365
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Revenue summary failed: {e}")
            return {"error": str(e)}
    
    async def get_dashboard_data(self) -> Dict:
        """Get data for dashboard display"""
        try:
            # Get dashboard metrics from database
            dashboard_metrics = await self.db.find_one("dashboard_metrics")
            
            # Get recent cycle history
            cycle_history = await self.db.to_list("cycle_history", 10)
            
            # Get recent logs
            recent_logs = await self.db.to_list("ariel_logs", 20)
            
            # Get current status
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
        """Access to quantum research component"""
        return self.matrix.quantum_research
    
    @property
    def neural(self):
        """Access to neural engine component"""
        return self.matrix.neural_engine
    
    @property
    def campaign_manager(self):
        """Access to campaign manager component"""
        return self.matrix.campaign_manager

class ArielDashboard:
    """Dashboard for monitoring Ariel performance"""
    
    def __init__(self):
        self.db = None
        self.metrics_cache = {}
        self.last_cache_update = None
    
    async def initialize(self, db):
        """Initialize dashboard with database connection"""
        self.db = db
        
        # Create dashboard data if not exists
        dashboard_data = await self.db.find_one("dashboard_metrics")
        if not dashboard_data:
            await self.db.insert_one("dashboard_metrics", {
                "initialized": True,
                "timestamp": datetime.utcnow().isoformat(),
                "total_cycles": 0,
                "total_revenue": 0.0
            })
    
    async def record_cycle_data(self, cycle_data: Dict):
        """Record cycle performance data"""
        try:
            await self.db.insert_one("cycle_history", cycle_data)
            
            # Update dashboard metrics
            await self.update_dashboard_metrics(cycle_data)
            
        except Exception as e:
            logger.error(f"Failed to record cycle data: {e}")
    
    async def update_dashboard_metrics(self, cycle_data: Dict):
        """Update dashboard metrics"""
        try:
            # Get current metrics
            current_metrics = await self.db.find_one("dashboard_metrics")
            
            if current_metrics:
                # Update metrics
                updated_metrics = {
                    **current_metrics,
                    "total_cycles": current_metrics.get("total_cycles", 0) + 1,
                    "total_revenue": current_metrics.get("total_revenue", 0) + cycle_data.get("revenue_generated", 0),
                    "last_cycle_duration": cycle_data.get("duration", 0),
                    "last_opportunities": cycle_data.get("opportunities_found", 0),
                    "last_updated": datetime.utcnow().isoformat()
                }
                
                # Store updated metrics (replace existing)
                await self.db.insert_one("dashboard_metrics", updated_metrics)
            
        except Exception as e:
            logger.error(f"Failed to update dashboard metrics: {e}")
    
    async def get_recent_activities(self, limit: int = 10) -> List[Dict]:
        """Get recent orchestrator activities"""
        try:
            activities = await self.db.to_list("ariel_logs", limit)
            return activities if activities else []
        except Exception as e:
            logger.error(f"Failed to get recent activities: {e}")
            return []
    
    async def get_performance_summary(self) -> Dict:
        """Get performance summary for dashboard"""
        try:
            # Get dashboard metrics
            metrics = await self.db.find_one("dashboard_metrics")
            
            # Get recent cycle history
            recent_cycles = await self.db.to_list("cycle_history", 10)
            
            # Calculate performance stats
            if recent_cycles:
                avg_duration = sum(cycle.get("duration", 0) for cycle in recent_cycles) / len(recent_cycles)
                avg_opportunities = sum(cycle.get("opportunities_found", 0) for cycle in recent_cycles) / len(recent_cycles)
                total_recent_revenue = sum(cycle.get("revenue_generated", 0) for cycle in recent_cycles)
            else:
                avg_duration = 0
                avg_opportunities = 0
                total_recent_revenue = 0
            
            return {
                "total_cycles": metrics.get("total_cycles", 0) if metrics else 0,
                "total_revenue": metrics.get("total_revenue", 0) if metrics else 0,
                "average_cycle_duration": avg_duration,
                "average_opportunities_per_cycle": avg_opportunities,
                "recent_revenue": total_recent_revenue,
                "recent_cycles_count": len(recent_cycles),
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get performance summary: {e}")
            return {"error": str(e)}
