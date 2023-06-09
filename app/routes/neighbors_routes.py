from flask import Blueprint, jsonify, request, make_response, current_app
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
from app import db 
from app.models.neighbors import Neighbor

neighbor_bp = Blueprint('neighbors', __name__, url_prefix = '/neighbors')

@neighbor_bp.route('', methods=['GET'])
def get_all_neighbors():
    neighbors = Neighbor.query.all()
    neighbor_list = []
    
    for neighbor in neighbors:
        neighbor_data = {
            'id': neighbor.neighbor_id,
            'name': neighbor.name,
            'zipcode': neighbor.zipcode,
            'email': neighbor.email,
            'phone': neighbor.phone,
            'services': neighbor.services,
            'skills': neighbor.skills
        }
        neighbor_list.append(neighbor_data)
    
    return jsonify(neighbor_list)

@neighbor_bp.route('/<neighbor_id>', methods=['GET'])
def get_neighbor(neighbor_id):
    neighbor = Neighbor.query.get(neighbor_id)

    if not neighbor:
        return jsonify({'message': 'Neighbor not found'}), 404

    neighbor_data = {
        'id': neighbor.neighbor_id,
        'name': neighbor.name,
        'zipcode': neighbor.zipcode,
        'email': neighbor.email,
        'phone': neighbor.phone,
        'services': neighbor.services,
        'skills': neighbor.skills
    }

    return jsonify(neighbor_data)



@neighbor_bp.route('/login', methods=['POST'])
def login():
    response = request.get_json()
    email = response['email']
    password = response['password']
    neighbor_id = request.json.get('neighbor_id')


    neighbor = Neighbor.query.filter_by(email=email).first()

    if neighbor and sha256.verify(password, neighbor.password):
        # Generate JWT token
        token = create_access_token(
            identity=neighbor.neighbor_id,
            expires_delta=timedelta(hours=1)
        )

        return jsonify({'token': token, "neighbor_id":neighbor.neighbor_id, 'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@neighbor_bp.route('/register', methods=['POST'])
def register():
    response = request.get_json()
    name = response['name']
    password = response['password']
    zipCode = response['zipcode']
    email = response['email']
    phone = response['phone']
    services = response['services']
    skills = response['skills']

    existing_neighbor = Neighbor.query.filter_by(email=email).first()
    if existing_neighbor:
        return jsonify({'message': 'Email already registered'}), 400

    hashed_password = sha256.hash(password)

    new_neighbor = Neighbor(
        name=name,
        password=hashed_password,
        zipcode=zipCode,
        email=email,
        phone=phone,
        services=services,
        skills=skills
    )
    db.session.add(new_neighbor)
    db.session.commit()

    # Generate JWT token
    token = create_access_token(
            identity=new_neighbor.neighbor_id,
            expires_delta=timedelta(hours=1)
        )

    return jsonify({'token': token, 'message': 'Registration successful'}), 201

@neighbor_bp.route('/<neighbor_id>/skills', methods=['PUT'])
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

@neighbor_bp.route('/<neighbor_id>/services', methods=['PATCH'])
def update_services(neighbor_id):
    neighbor = Neighbor.query.get(neighbor_id)
    if not neighbor:
        return jsonify({'message': 'Neighbor not found'}), 404

    response = request.get_json()
    services = response.get('services')

    if not services:
        return jsonify({'message': 'No services provided'}), 400

    neighbor.services = services
    db.session.commit()

    return jsonify({'message': 'Services updated successfully'})

