import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from ariel_matrix.ariel_user import ARIEL, ArielUser

logger = logging.getLogger("ArielMatrix.APIManager")

class APIManager:
    def __init__(self):
        self.apis = []
        self.api_keys = {}
        self.rate_limits = {}
        self.last_sync = None
        self.rotation_schedule = {}

    async def sync_apis(self):
        logger.info("Syncing APIs...")
        try:
            await self._rotate_keys()
            await self._health_check_all()
            await self._update_rate_limits()
            await self._auto_register_apis()
            self.last_sync = datetime.utcnow()
            logger.info(f"API sync completed. Managing {len(self.apis)} APIs")
        except Exception as e:
            logger.error(f"API sync failed: {e}")
            raise

    async def _rotate_keys(self):
        for api_name in self.api_keys:
            self.api_keys[api_name]['key'] = ARIEL._generate_api_key()
            self.api_keys[api_name]['last_rotation'] = datetime.utcnow().isoformat()

    async def _health_check_all(self):
        # Real implementation would use ARIEL's identity for secure checks
        for api in self.apis:
            api['health'] = {'status': 'healthy', 'last_check': datetime.utcnow().isoformat()}

    async def _update_rate_limits(self):
        for api in self.apis:
            api_name = api.get('name')
            if api_name:
                self.rate_limits[api_name] = {
                    'requests_per_minute': 1000,
                    'requests_used': 0,
                    'reset_time': (datetime.utcnow() + timedelta(minutes=1)).isoformat()
                }

    async def _auto_register_apis(self):
        # Only allow ARIEL to register new APIs, each with a cryptographic key
        potential_apis = [
            {'name': 'affiliate_network_1', 'type': 'affiliate', 'priority': 'high'},
            {'name': 'social_media_api', 'type': 'social', 'priority': 'medium'},
            {'name': 'analytics_service', 'type': 'analytics', 'priority': 'low'}
        ]
        for api_config in potential_apis:
            if not self._api_exists(api_config['name']):
                await self.register_api(api_config)

    def _api_exists(self, api_name: str) -> bool:
        return any(api.get('name') == api_name for api in self.apis)

    async def register_api(self, api_config: Dict):
        api_name = api_config.get('name')
        if not api_name:
            raise ValueError("API name is required")
        if self._api_exists(api_name):
            logger.warning(f"API {api_name} already registered")
            return
        key = ARIEL._generate_api_key()
        full_config = {
            'name': api_name,
            'type': api_config.get('type', 'unknown'),
            'priority': api_config.get('priority', 'medium'),
            'registered_at': datetime.utcnow().isoformat(),
            'status': 'active',
            'api_key': key,
            'health': {'status': 'unknown'}
        }
        self.apis.append(full_config)
        self.api_keys[api_name] = {'key': key, 'created_by': ARIEL.user_id, 'last_rotation': datetime.utcnow().isoformat()}
        self.rotation_schedule[api_name] = {'interval_hours': api_config.get('rotation_hours', 24), 'last_rotation': datetime.utcnow().isoformat()}
        logger.info(f"Registered new API: {api_name}")

    def get_api_key(self, api_name: str) -> Optional[str]:
        api_data = self.api_keys.get(api_name)
        if api_data:
            return api_data.get('key')
        return None

    async def get_summary(self) -> Dict:
        healthy_apis = sum(1 for api in self.apis if api.get('health', {}).get('status') == 'healthy')
        return {
            'total_apis': len(self.apis),
            'healthy_apis': healthy_apis,
            'unhealthy_apis': len(self.apis) - healthy_apis,
            'total_keys': len(self.api_keys),
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'apis': [api.get('name') for api in self.apis]
        }
