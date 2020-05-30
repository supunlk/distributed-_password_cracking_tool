import worker
import master
import requests
import json


class WorkThread:
    def __init__(self):
        self.worker = None
        self.master = None

        self.master_node = None
        self.slave_node = None

    def init_worker(self, master_node, slave_node):
        self.worker = worker.Worker(self.check_password_is_cracked)
        self.slave_node = slave_node
        self.master_node = master_node

    def set_worker_password_range(self, pw_range):
        if self.worker:
            self.worker.set_password_range(pw_range)
        else:
            raise Exception()

    def init_master(self, get_workers_fn):
        self.master = master.Master(get_workers_fn)

    def check_password_is_cracked(self, password):
        url = f"{self.master_node['address']}:{self.master_node['port']}/check-password"
        response = requests.post(url, json={'password': password, 'node': self.slave_node['service_id']})
        response_json = json.loads(response.content)
        return response_json['is_cracked']
