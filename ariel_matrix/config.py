import os
from typing import Dict, Any, Optional

# Configuration settings for ArielMatrix
CONFIG = {
    # System Configuration
    "max_bots": int(os.getenv("ARIEL_MAX_BOTS", "100")),
    "log_level": os.getenv("ARIEL_LOG_LEVEL", "INFO"),
    "cycle_interval": int(os.getenv("ARIEL_CYCLE_INTERVAL", "1800")),  # seconds
    "debug_mode": os.getenv("ARIEL_DEBUG", "false").lower() == "true",
    
    # Database Configuration
    "database_url": os.getenv("DATABASE_URL", "sqlite:///data/ariel.db"),
    "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379"),
    "mongodb_url": os.getenv("MONGODB_URI"),
    
    # API Configuration
    "api_rate_limit": int(os.getenv("ARIEL_API_RATE_LIMIT", "1000")),  # requests per hour
    "api_timeout": int(os.getenv("ARIEL_API_TIMEOUT", "30")),  # seconds
    "webhook_secret": os.getenv("ARIEL_WEBHOOK_SECRET", "default_secret"),
    
    # Security Configuration
    "encryption_key": os.getenv("ARIEL_ENCRYPTION_KEY"),
    "jwt_secret": os.getenv("JWT_SECRET", "default_jwt_secret"),
    "allowed_origins": os.getenv("ALLOWED_ORIGINS", "*").split(","),
    
    # Neural Engine Configuration
    "neural_model_path": os.getenv("NEURAL_MODEL_PATH", "models/"),
    "neural_batch_size": int(os.getenv("NEURAL_BATCH_SIZE", "32")),
    "neural_learning_rate": float(os.getenv("NEURAL_LEARNING_RATE", "0.001")),
    
    # Quantum Research Configuration
    "quantum_provider": os.getenv("QUANTUM_PROVIDER", "simulator"),
    "ibmq_token": os.getenv("IBMQ_TOKEN"),
    "aws_braket_region": os.getenv("AWS_BRAKET_REGION", "us-east-1"),
    
    # Web Scraping Configuration
    "scraping_delay": float(os.getenv("SCRAPING_DELAY", "1.0")),  # seconds between requests
    "scraping_timeout": int(os.getenv("SCRAPING_TIMEOUT", "10")),  # seconds
    "scraping_user_agent": os.getenv("SCRAPING_USER_AGENT", "ArielMatrix/1.0"),
    "max_concurrent_scrapes": int(os.getenv("MAX_CONCURRENT_SCRAPES", "5")),
    
    # Campaign Management Configuration
    "default_campaign_budget": float(os.getenv("DEFAULT_CAMPAIGN_BUDGET", "100.0")),
    "max_campaign_duration": int(os.getenv("MAX_CAMPAIGN_DURATION", "30")),  # days
    "campaign_optimization_threshold": float(os.getenv("CAMPAIGN_OPTIMIZATION_THRESHOLD", "0.1")),
    
    # Asset Management Configuration
    "asset_acquisition_budget": float(os.getenv("ASSET_ACQUISITION_BUDGET", "1000.0")),
    "asset_renewal_days": int(os.getenv("ASSET_RENEWAL_DAYS", "30")),
    "max_assets_per_type": int(os.getenv("MAX_ASSETS_PER_TYPE", "10")),
    
    # Discovery Configuration
    "discovery_keywords": os.getenv("DISCOVERY_KEYWORDS", "opportunity,reward,bounty,contest,grant").split(","),
    "max_opportunities_per_source": int(os.getenv("MAX_OPPORTUNITIES_PER_SOURCE", "20")),
    "opportunity_value_threshold": int(os.getenv("OPPORTUNITY_VALUE_THRESHOLD", "65")),
    
    # Scheduler Configuration
    "scheduler_timezone": os.getenv("SCHEDULER_TIMEZONE", "UTC"),
    "max_concurrent_tasks": int(os.getenv("MAX_CONCURRENT_TASKS", "10")),
    "task_retry_attempts": int(os.getenv("TASK_RETRY_ATTEMPTS", "3")),
    
    # Reporter Configuration
    "email_smtp_server": os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com"),
    "email_smtp_port": int(os.getenv("EMAIL_SMTP_PORT", "587")),
    "email_username": os.getenv("EMAIL_USERNAME"),
    "email_password": os.getenv("EMAIL_PASSWORD"),
    "report_recipients": os.getenv("REPORT_RECIPIENTS", "").split(",") if os.getenv("REPORT_RECIPIENTS") else [],
    
    # Reward Manager Configuration
    "reward_pool_size": float(os.getenv("REWARD_POOL_SIZE", "10000.0")),
    "reward_distribution_threshold": float(os.getenv("REWARD_DISTRIBUTION_THRESHOLD", "100.0")),
    "max_reward_per_action": float(os.getenv("MAX_REWARD_PER_ACTION", "500.0")),
    
    # Plugin Configuration
    "plugin_directory": os.getenv("PLUGIN_DIRECTORY", "plugins/"),
    "plugin_auto_load": os.getenv("PLUGIN_AUTO_LOAD", "true").lower() == "true",
    "plugin_sandbox": os.getenv("PLUGIN_SANDBOX", "true").lower() == "true",
    
    # Ethics and Compliance Configuration
    "ethics_strict_mode": os.getenv("ETHICS_STRICT_MODE", "true").lower() == "true",
    "compliance_check_interval": int(os.getenv("COMPLIANCE_CHECK_INTERVAL", "3600")),  # seconds
    "gdpr_compliance": os.getenv("GDPR_COMPLIANCE", "true").lower() == "true",
    
    # Performance Configuration
    "max_memory_usage": int(os.getenv("MAX_MEMORY_USAGE", "1024")),  # MB
    "max_cpu_usage": int(os.getenv("MAX_CPU_USAGE", "80")),  # percentage
    "performance_monitoring": os.getenv("PERFORMANCE_MONITORING", "true").lower() == "true",
    
    # External Service Configuration
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
    "paystack_secret_key": os.getenv("PAYSTACK_SECRET_KEY"),
    "stripe_secret_key": os.getenv("STRIPE_SECRET_KEY"),
    "sendgrid_api_key": os.getenv("SENDGRID_API_KEY"),
    "twilio_account_sid": os.getenv("TWILIO_ACCOUNT_SID"),
    "twilio_auth_token": os.getenv("TWILIO_AUTH_TOKEN"),
    
    # Feature Flags
    "enable_quantum_research": os.getenv("ENABLE_QUANTUM_RESEARCH", "true").lower() == "true",
    "enable_neural_engine": os.getenv("ENABLE_NEURAL_ENGINE", "true").lower() == "true",
    "enable_web_scraping": os.getenv("ENABLE_WEB_SCRAPING", "true").lower() == "true",
    "enable_bot_deployment": os.getenv("ENABLE_BOT_DEPLOYMENT", "true").lower() == "true",
    "enable_auto_campaigns": os.getenv("ENABLE_AUTO_CAMPAIGNS", "true").lower() == "true",
    "enable_asset_management": os.getenv("ENABLE_ASSET_MANAGEMENT", "true").lower() == "true",
}

class Config:
    """Configuration wrapper for ArielMatrix"""
    def __init__(self):
        self.config = CONFIG.copy()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple configuration values"""
        self.config.update(updates)
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database-related configuration"""
        return {
            "database_url": self.get("database_url"),
            "redis_url": self.get("redis_url"),
            "mongodb_url": self.get("mongodb_url")
        }
    
    def get_api_config(self) -> Dict[str, Any]:
        """Get API-related configuration"""
        return {
            "rate_limit": self.get("api_rate_limit"),
            "timeout": self.get("api_timeout"),
            "webhook_secret": self.get("webhook_secret")
        }
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get security-related configuration"""
        return {
            "encryption_key": self.get("encryption_key"),
            "jwt_secret": self.get("jwt_secret"),
            "allowed_origins": self.get("allowed_origins")
        }
    
    def get_neural_config(self) -> Dict[str, Any]:
        """Get neural engine configuration"""
        return {
            "model_path": self.get("neural_model_path"),
            "batch_size": self.get("neural_batch_size"),
            "learning_rate": self.get("neural_learning_rate")
        }
    
    def get_quantum_config(self) -> Dict[str, Any]:
        """Get quantum research configuration"""
        return {
            "provider": self.get("quantum_provider"),
            "ibmq_token": self.get("ibmq_token"),
            "aws_braket_region": self.get("aws_braket_region")
        }
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled"""
        feature_key = f"enable_{feature}"
        return self.get(feature_key, False)
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate configuration and return any issues"""
        issues = []
        warnings = []
        
        # Check required configurations
        required_keys = ["database_url", "jwt_secret"]
        for key in required_keys:
            if not self.get(key):
                issues.append(f"Missing required configuration: {key}")
        
        # Check optional but recommended configurations
        recommended_keys = ["encryption_key", "email_username", "openai_api_key"]
        for key in recommended_keys:
            if not self.get(key):
                warnings.append(f"Missing recommended configuration: {key}")
        
        # Validate numeric ranges
        if self.get("max_bots", 0) > 1000:
            warnings.append("max_bots is very high, consider reducing for performance")
        
        if self.get("api_rate_limit", 0) < 100:
            warnings.append("api_rate_limit is very low, may impact functionality")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }

# Global configuration instance
config = Config()

def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value (convenience function)"""
    return config.get(key, default)

def set_config(key: str, value: Any) -> None:
    """Set configuration value (convenience function)"""
    config.set(key, value)
