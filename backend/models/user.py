from database import db
from datetime import datetime
import hashlib

class User:
    collection = db.get_collection('users')
    
    @staticmethod
    def create(username, email, password):
        """Create a new user"""
        if User.find_by_email(email):
            return None, "Email already exists"
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'created_at': datetime.utcnow(),
            'status': 'active',
            'profile_pic': None,
            'bio': ''
        }
        result = User.collection.insert_one(user_data)
        return str(result.inserted_id), "User created successfully"
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        return User.collection.find_one({'email': email})
    
    @staticmethod
    def find_by_username(username):
        """Find user by username"""
        return User.collection.find_one({'username': username})
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        from bson import ObjectId
        return User.collection.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def verify_password(email, password):
        """Verify user password"""
        user = User.find_by_email(email)
        if not user:
            return None
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user['password'] == hashed_password:
            return user
        return None
