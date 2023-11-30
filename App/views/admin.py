from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from App.controllers.admin import (
    create_admin,
    get_all_admins_json,
    update_admin,
    get_admin_json,
    get_admin_by_username

)


admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

@admin_views.route('/api/admins', methods=['GET'])
def get_all_admins_action():
    admins = get_all_admins_json()
    return (admins,200)

@admin_views.route('/api/admins/<int:admin_id>', methods=['GET'])
def get_admin_action(admin_id):
    admin = get_admin_json(admin_id)
    if admin:
        return (admin,200)
    return (jsonify({'error': f"Admin not found."}),400)

@admin_views.route('/api/admins', methods=['POST'])
def create_admin_action():
    data = request.form

    response = get_admin_by_username(data['username'])

    if response:
        return (jsonify({'error': f"Admin {data['username']} already exist"}),400)


    response = create_admin(data['username'],data['email'],data['password'])
    if response:
        return (jsonify({'message': f"Admin created"}),201)
    return (jsonify({'error': f"Error creating Admin"}),400)

@admin_views.route('/api/admins', methods=['PUT'])
def update_competitor_endpoint():
    data = request.form
    admin_id = request.args.get('id')
    admin_id = int(admin_id)
    print(admin_id)
    updated = update_admin(
        admin_id,
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    print(updated)
    if updated:
        return jsonify({'message': f"Admin {admin_id} updated"}), 200
    return jsonify({'error': f"Error updating admin {admin_id}"}), 400


