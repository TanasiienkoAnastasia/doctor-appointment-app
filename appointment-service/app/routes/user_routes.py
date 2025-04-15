from flask import Blueprint, request, jsonify
from app import db

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = UserProfile(
        username=data['username'],
        full_name=data['full_name'],
        email=data['email'],
        role=data['role']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Користувача створено'}), 201

@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserProfile.query.get(user_id)
    if not user:
        return jsonify({'message': 'Користувача не знайдено'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'full_name': user.full_name,
        'email': user.email,
        'role': user.role
    })

@user_routes.route('/users', methods=['GET'])
def get_all_users():
    users = UserProfile.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'full_name': user.full_name,
        'email': user.email,
        'role': user.role
    } for user in users])
