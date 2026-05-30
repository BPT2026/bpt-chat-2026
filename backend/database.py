from pymongo import MongoClient
from config import Config
import os

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        try:
            self.client = MongoClient(Config.MONGODB_URI)
            self.db = self.client[Config.DB_NAME]
            # Test connection
            self.client.admin.command('ping')
            print(f"✓ Connected to MongoDB: {Config.DB_NAME}")
        except Exception as e:
            print(f"✗ Failed to connect to MongoDB: {e}")
            raise
    
    def get_collection(self, collection_name):
        return self.db[collection_name]
    
    def close(self):
        if self.client:
            self.client.close()

# Initialize database
db = Database()
