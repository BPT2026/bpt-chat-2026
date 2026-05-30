from database import db
from datetime import datetime
from bson import ObjectId

class Message:
    collection = db.get_collection('messages')
    
    @staticmethod
    def create(sender_id, receiver_id, content, message_type='text', file_url=None):
        """Create a new message"""
        message_data = {
            'sender_id': ObjectId(sender_id),
            'receiver_id': ObjectId(receiver_id),
            'content': content,
            'message_type': message_type,  # 'text' or 'file'
            'file_url': file_url,
            'created_at': datetime.utcnow(),
            'read': False
        }
        result = Message.collection.insert_one(message_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_chat_history(user_id, contact_id, limit=50):
        """Get chat history between two users"""
        messages = list(Message.collection.find({
            '$or': [
                {'sender_id': ObjectId(user_id), 'receiver_id': ObjectId(contact_id)},
                {'sender_id': ObjectId(contact_id), 'receiver_id': ObjectId(user_id)}
            ]
        }).sort('created_at', -1).limit(limit))
        
        # Convert ObjectId to string for JSON serialization
        for msg in messages:
            msg['_id'] = str(msg['_id'])
            msg['sender_id'] = str(msg['sender_id'])
            msg['receiver_id'] = str(msg['receiver_id'])
            msg['created_at'] = msg['created_at'].isoformat()
        
        return list(reversed(messages))
    
    @staticmethod
    def mark_as_read(message_id):
        """Mark message as read"""
        Message.collection.update_one(
            {'_id': ObjectId(message_id)},
            {'$set': {'read': True}}
        )
    
    @staticmethod
    def get_unread_count(user_id):
        """Get unread message count"""
        return Message.collection.count_documents({
            'receiver_id': ObjectId(user_id),
            'read': False
        })
