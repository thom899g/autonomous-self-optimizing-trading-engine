"""
Configuration management for trading engine.
Centralizes all configurable parameters with environment-aware defaults.
"""
import os
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class TradingConfig:
    """Main configuration dataclass for trading parameters."""
    
    # Data Collection
    DATA_SOURCES: Dict[str, Any] = None
    UPDATE_INTERVAL: int = 60  # seconds
    HISTORICAL_DAYS: int = 365
    
    # RL Agent
    RL_EPISODES: int = 1000
    RL_LEARNING_RATE: float = 0.001
    RL_DISCOUNT_FACTOR: float = 0.95
    RL_EXPLORATION_RATE: float = 0.1
    
    # Risk Management
    MAX_POSITION_SIZE: float = 0.1  # 10% of portfolio
    STOP_LOSS_PERCENT: float = 0.02  # 2%
    MAX_DRAWDOWN: float = 0.15  # 15%
    
    # Execution
    PAPER_TRADING: bool = True
    ORDER_TIMEOUT: int = 30  # seconds
    MIN_LIQUIDITY: float = 10000.0
    
    # Firebase
    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_CREDENTIALS_PATH: str = "firebase_credentials.json"
    
    def __post_init__(self):
        """Initialize with environment variables or defaults."""
        self.DATA_SOURCES = {
            'crypto': os.getenv('CRYPTO_EXCHANGE', 'binance'),
            'stocks': os.getenv('STOCKS_API', 'yfinance'),
            'news': os.getenv('NEWS_API', 'newsapi.org')
        }
        self.PAPER_TRADING = os.getenv('PAPER_TRADING', 'True').lower() == 'true'
        self.FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID', '')
        
        # Validate critical configs
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate configuration parameters."""
        if self.MAX_POSITION_SIZE <= 0 or self.MAX_POSITION_SIZE > 1:
            raise ValueError("MAX_POSITION_SIZE must be between 0 and 1")
        if self.STOP_LOSS_PERCENT <= 0:
            raise ValueError("STOP_LOSS_PERCENT must be positive")
        if not self.FIREBASE_PROJECT_ID and not self.PAPER_TRADING:
            logging.warning("Firebase project ID not set - some features disabled")

# Global config instance
config = TradingConfig()