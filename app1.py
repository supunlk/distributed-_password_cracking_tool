from flask import Flask, jsonify, request
from service_discovery import ServiceDiscovery
from bully import Bully
import json
import logging
import sys

PORT = int(sys.argv[1])
assert PORT
SERVICE_ID = f'service_{PORT}'
NAME = f's_{PORT}'
HOST = 'http://localhost'

logging.basicConfig(filename=f"{SERVICE_ID}.log", level=logging.INFO)

app = Flask(__name__)
service_discovery = ServiceDiscovery()

service = service_discovery.register(service_id=SERVICE_ID, name=NAME, address=HOST, port=PORT)
bully = Bully(service, service_discovery.list)
service_details = bully.get_service()

print('Node Id is ', service_details['service_id'])


@app.route('/election', methods=['POST'])
def hello_world():
    data = json.loads(request.data)
    bully.init_election(False, True)
    return jsonify({'data': 'ok'})


@app.route('/node-info', methods=['POST'])
def node_info():
    data = json.loads(request.data)
    bully.update_service_list(data)
    return jsonify({'data': service_details})


@app.route('/ongoing-election-info', methods=['POST'])
def ongoing_election_info():
    data = json.loads(request.data)
    bully.ongoing_election = data['ongoing_election']
    return jsonify({'data': 'updated'})


@app.route('/coordinator', methods=['POST'])
def coordinator_msg():
    data = json.loads(request.data)
    bully.update_leader(data)
    return jsonify({'data': 'updated'})


@app.route('/worker-instructions', methods=['POST'])
def worker_instructions():
    data = json.loads(request.data)
    bully.set_password_range(data)
    return jsonify({'data': 'starting work'})


@app.route('/check-password', methods=['POST'])
def check_password():
    data = json.loads(request.data)
    is_cracked = bully.compare_pw(data)
    return jsonify({'is_cracked': is_cracked})


@app.route('/stop-password-cracking', methods=['POST'])
def stop_password_cracking():
    data = json.loads(request.data)
    bully.stop_password_cracking()
    return jsonify({'is_cracked': True})


if __name__ == '__main__':
    app.run(port=PORT)

print("__________________________")
print("deregister", service['ID'])
service_discovery.deregister(service['ID'])
