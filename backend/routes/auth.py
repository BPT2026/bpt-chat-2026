from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from routes import auth_bp
from models.user import User

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user_id, message = User.create(data['username'], data['email'], data['password'])
    
    if user_id:
        access_token = create_access_token(identity=user_id)
        return jsonify({
            'message': message,
            'user_id': user_id,
            'access_token': access_token
        }), 201
    else:
        return jsonify({'error': message}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = User.verify_password(data['email'], data['password'])
    
    if user:
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify({
            'message': 'Login successful',
            'user_id': str(user['_id']),
            'username': user['username'],
            'email': user['email'],
            'access_token': access_token
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    user_id = get_jwt_identity()
    user = User.find_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user_id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
        'bio': user.get('bio', ''),
        'profile_pic': user.get('profile_pic'),
        'status': user.get('status', 'active')
    }), 200
