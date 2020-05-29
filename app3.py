from flask import Flask, jsonify, request
from service_discovery import ServiceDiscovery
from bully import Bully
import json
import logging

logging.basicConfig(filename='demo.log', level=logging.INFO)

PORT = 5003
SERVICE_ID = f'service_{PORT}'
NAME = f's_{PORT}'
HOST = 'http://localhost'

app = Flask(__name__)
service_discovery = ServiceDiscovery()

service = service_discovery.register(service_id=SERVICE_ID, name=NAME, address=HOST, port=PORT)
bully = Bully(service, service_discovery.list)
service_details = bully.get_service()

print('Node Id is ', service_details['service_id'])


@app.route('/election', methods=['POST'])
def hello_world():
    data = json.loads(request.data)
    print('election message received...', data['service_id'])
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
    bully.update_leader()
    return jsonify({'data': 'updated'})


if __name__ == '__main__':
    app.run(port=PORT)

print("__________________________")
print("deregister", service['ID'])
service_discovery.deregister(service['ID'])
