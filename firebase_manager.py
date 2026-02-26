"""
Firebase Firestore integration for state persistence and real-time updates.
Handles all database operations with proper error handling.
"""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client
from google.api_core.exceptions import GoogleAPIError

from config import config

class FirebaseManager:
    """Manages Firebase Firestore connections and operations."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern for Firebase connection."""
        if cls._instance is None:
            cls._instance = super(FirebaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize Firebase connection if not already initialized."""
        if not self._initialized:
            try:
                # Initialize with credentials file
                if not config.FIREBASE_PROJECT_ID:
                    logging.warning("Firebase project ID not configured")
                    self.db = None
                    return
                    
                cred = credentials.Certificate(config.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred, {
                    'projectId': config.FIREBASE_PROJECT_ID
                })
                self.db: Client = firestore.client()
                self._initialized =