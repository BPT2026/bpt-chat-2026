from database import db
from datetime import datetime
from bson import ObjectId

class Contact:
    collection = db.get_collection('contacts')
    
    @staticmethod
    def add_contact(user_id, contact_user_id, contact_name=None):
        """Add a contact"""
        # Check if already exists
        if Contact.collection.find_one({
            'user_id': ObjectId(user_id),
            'contact_user_id': ObjectId(contact_user_id)
        }):
            return None, "Contact already exists"
        
        contact_data = {
            'user_id': ObjectId(user_id),
            'contact_user_id': ObjectId(contact_user_id),
            'contact_name': contact_name,
            'added_at': datetime.utcnow()
        }
        result = Contact.collection.insert_one(contact_data)
        return str(result.inserted_id), "Contact added successfully"
    
    @staticmethod
    def get_contacts(user_id):
        """Get all contacts for a user"""
        contacts = list(Contact.collection.find({
            'user_id': ObjectId(user_id)
        }))
        
        for contact in contacts:
            contact['_id'] = str(contact['_id'])
            contact['user_id'] = str(contact['user_id'])
            contact['contact_user_id'] = str(contact['contact_user_id'])
            contact['added_at'] = contact['added_at'].isoformat()
        
        return contacts
    
    @staticmethod
    def remove_contact(user_id, contact_user_id):
        """Remove a contact"""
        Contact.collection.delete_one({
            'user_id': ObjectId(user_id),
            'contact_user_id': ObjectId(contact_user_id)
        })
