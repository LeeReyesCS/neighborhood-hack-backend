from flask import Blueprint, jsonify, request, make_response
from passlib.hash import pbkdf2_sha256 as sha256
from app import db 

from app.models.neighbors import Neighbor

board_bp = Blueprint('board', __name__, url_prefix = '/neighbors')

@app.route('/login', methods=['POST'])
def login():
    response = request.get_json()
    username = response['username']
    password = response['password']

    # Find the user in your database or storage mechanism
    user = next((user for user in users if user['username'] == username), None)

    if user and sha256.verify(password, user['password']):
        return 'Login successful'
    else:
        return 'Invalid username or password'


@app.route('/register', methods=['POST'])
def register():
    response = request.get_json()
    username = response['username']
    password = response['password']
    name = response['name']
    zipcode = response['zipcode']
    email = response['email']
    phone = response['phone']
    services = response['services']
    skills = response ['skills']

    hashed_password = sha256.hash(password)

    # Store the user in your database or storage mechanism
    users.append({'username': username, 'password': hashed_password})

    return 'Registration successful'

@app.route('/<neighbor_id>/skills', methods=['PUT'])
def update_skills(neighbor_id):
    neighbor = Neighbor.query.get(neighbor_id)
    if not neighbor:
        return jsonify({'message': 'Neighbor not found'}), 404

    data = request.get_json()
    skills = data.get('skills')

    if not skills:
        return jsonify({'message': 'No skills provided'}), 400

    neighbor.skills = skills
    db.session.commit()

    return jsonify({'message': 'Skills updated successfully'})

@app.route('/<neighbor_id>/services', methods=['PATCH'])
def update_services(neighbor_id):
    neighbor = Neighbor.query.get(neighbor_id)
    if not neighbor:
        return jsonify({'message': 'Neighbor not found'}), 404

    data = request.get_json()
    services = data.get('services')

    if not services:
        return jsonify({'message': 'No services provided'}), 400

    neighbor.services = services
    db.session.commit()

    return jsonify({'message': 'Services updated successfully'})

