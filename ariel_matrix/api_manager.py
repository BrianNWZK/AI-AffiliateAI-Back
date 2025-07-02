import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
import random
import string

logger = logging.getLogger("ArielMatrix.APIManager")

class APIManager:
    def __init__(self):
        self.apis = []
        self.api_keys = {}
        self.rate_limits = {}
        self.last_sync = None
        self.rotation_schedule = {}
        
    async def sync_apis(self):
        """Sync and manage all registered APIs"""
        logger.info("Syncing APIs...")
        
        try:
            # Rotate API keys if needed
            await self._rotate_keys()
            
            # Check API health
            await self._health_check_all()
            
            # Update rate limits
            await self._update_rate_limits()
            
            # Register new APIs if needed
            await self._auto_register_apis()
            
            self.last_sync = datetime.utcnow()
            logger.info(f"API sync completed. Managing {len(self.apis)} APIs")
            
        except Exception as e:
            logger.error(f"API sync failed: {e}")
            raise
    
    async def _rotate_keys(self):
        """Rotate API keys based on schedule"""
        current_time = datetime.utcnow()
        
        for api_name, schedule in self.rotation_schedule.items():
            if api_name in self.api_keys:
                last_rotation = schedule.get('last_rotation')
                interval_hours = schedule.get('interval_hours', 24)
                
                if last_rotation:
                    last_rotation_time = datetime.fromisoformat(last_rotation)
                    if current_time - last_rotation_time > timedelta(hours=interval_hours):
                        await self._rotate_api_key(api_name)
                else:
                    # First rotation
                    await self._rotate_api_key(api_name)
    
    async def _rotate_api_key(self, api_name: str):
        """Rotate a specific API key"""
        logger.info(f"Rotating API key for {api_name}")
        
        try:
            # Generate new API key (simulation)
            new_key = self._generate_api_key()
            
            # Update key
            old_key = self.api_keys.get(api_name, {}).get('key')
            self.api_keys[api_name] = {
                'key': new_key,
                'created_at': datetime.utcnow().isoformat(),
                'previous_key': old_key,
                'status': 'active'
            }
            
            # Update rotation schedule
            if api_name not in self.rotation_schedule:
                self.rotation_schedule[api_name] = {}
            self.rotation_schedule[api_name]['last_rotation'] = datetime.utcnow().isoformat()
            
            logger.info(f"API key rotated successfully for {api_name}")
            
        except Exception as e:
            logger.error(f"Failed to rotate API key for {api_name}: {e}")
    
    def _generate_api_key(self, length: int = 32) -> str:
        """Generate a random API key"""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    async def _health_check_all(self):
        """Perform health checks on all APIs"""
        for api in self.apis:
            await self._health_check_api(api)
    
    async def _health_check_api(self, api: Dict):
        """Health check for a specific API"""
        api_name = api.get('name', 'unknown')
        
        try:
            # Simulate API health check
            await asyncio.sleep(0.1)
            
            # Random health status for simulation
            is_healthy = random.random() > 0.1  # 90% success rate
            
            api['health'] = {
                'status': 'healthy' if is_healthy else 'unhealthy',
                'last_check': datetime.utcnow().isoformat(),
                'response_time': random.uniform(0.1, 2.0)
            }
            
            if not is_healthy:
                logger.warning(f"API {api_name} health check failed")
            
        except Exception as e:
            logger.error(f"Health check failed for {api_name}: {e}")
            api['health'] = {
                'status': 'error',
                'last_check': datetime.utcnow().isoformat(),
                'error': str(e)
            }
    
    async def _update_rate_limits(self):
        """Update rate limit information for all APIs"""
        for api in self.apis:
            api_name = api.get('name')
            if api_name:
                # Simulate rate limit check
                self.rate_limits[api_name] = {
                    'requests_per_minute': random.randint(100, 1000),
                    'requests_used': random.randint(0, 50),
                    'reset_time': (datetime.utcnow() + timedelta(minutes=1)).isoformat()
                }
    
    async def _auto_register_apis(self):
        """Automatically register new APIs based on discovery"""
        # Simulate discovering new APIs
        potential_apis = [
            {'name': 'affiliate_network_1', 'type': 'affiliate', 'priority': 'high'},
            {'name': 'social_media_api', 'type': 'social', 'priority': 'medium'},
            {'name': 'analytics_service', 'type': 'analytics', 'priority': 'low'}
        ]
        
        for api_config in potential_apis:
            if not self._api_exists(api_config['name']):
                if random.random() > 0.7:  # 30% chance to register
                    await self.register_api(api_config)
    
    def _api_exists(self, api_name: str) -> bool:
        """Check if API is already registered"""
        return any(api.get('name') == api_name for api in self.apis)
    
    async def register_api(self, api_config: Dict):
        """Register a new API"""
        api_name = api_config.get('name')
        if not api_name:
            raise ValueError("API name is required")
        
        if self._api_exists(api_name):
            logger.warning(f"API {api_name} already registered")
            return
        
        # Create full API configuration
        full_config = {
            'name': api_name,
            'type': api_config.get('type', 'unknown'),
            'priority': api_config.get('priority', 'medium'),
            'registered_at': datetime.utcnow().isoformat(),
            'status': 'active',
            'health': {'status': 'unknown'}
        }
        
        self.apis.append(full_config)
        
        # Generate initial API key
        await self._rotate_api_key(api_name)
        
        # Set rotation schedule
        self.rotation_schedule[api_name] = {
            'interval_hours': api_config.get('rotation_hours', 24),
            'last_rotation': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Registered new API: {api_name}")
    
    def get_api_key(self, api_name: str) -> Optional[str]:
        """Get current API key for a service"""
        api_data = self.api_keys.get(api_name)
        if api_data and api_data.get('status') == 'active':
            return api_data.get('key')
        return None
    
    def get_api_status(self, api_name: str) -> Optional[Dict]:
        """Get status information for an API"""
        for api in self.apis:
            if api.get('name') == api_name:
                return {
                    'name': api_name,
                    'status': api.get('status'),
                    'health': api.get('health', {}),
                    'rate_limit': self.rate_limits.get(api_name, {}),
                    'key_status': self.api_keys.get(api_name, {}).get('status')
                }
        return None
    
    async def get_summary(self) -> Dict:
        """Get API management summary"""
        healthy_apis = sum(1 for api in self.apis if api.get('health', {}).get('status') == 'healthy')
        
        return {
            'total_apis': len(self.apis),
            'healthy_apis': healthy_apis,
            'unhealthy_apis': len(self.apis) - healthy_apis,
            'total_keys': len(self.api_keys),
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'apis': [api.get('name') for api in self.apis]
        }
    
    def remove_api(self, api_name: str):
        """Remove an API from management"""
        self.apis = [api for api in self.apis if api.get('name') != api_name]
        self.api_keys.pop(api_name, None)
        self.rate_limits.pop(api_name, None)
        self.rotation_schedule.pop(api_name, None)
        logger.info(f"Removed API: {api_name}")
