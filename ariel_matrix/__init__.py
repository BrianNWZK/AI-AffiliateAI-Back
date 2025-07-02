# Marks ariel_matrix as a Python package.
"""
ArielMatrix: Advanced AI appendage system for Ariel Orchestrator
Provides extended functionality for aggregation, API management, and more.
"""

from .aggregator import Aggregator
from .api_manager import APIManager

__version__ = "1.0.0"
__all__ = ["Aggregator", "APIManager"]
