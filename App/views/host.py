from flask import Blueprint, jsonify, request

from App.controllers import (
  create_host,
  get_host_by_organizationName
)

host_views = Blueprint('host_views', __name__, template_folder='../templates')


@host_views.route('/host/<string:name>', methods=['GET'])
def get_host_by_name(name):
    host = get_host_by_organizationName(name)
    if not host:
        return jsonify({'error': 'host not found'}), 404
    return (jsonify(host.toDict()),200)

@host_views.route('/host', methods=['POST'])
def make_host():
    data = request.form
    host = create_host(data['name'])
    if host:
       print(host.toDict())
       return (jsonify({'message': f"host created"}), 201)
    return (jsonify({'error': f"error creating host"}),400)