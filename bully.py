import datetime
import random
import requests
import threading
import json
import work_thread


class Bully:
    def __init__(self, service, get_service_list_fn, is_leader=False):
        self.service_id = datetime.datetime.now().microsecond + random.randint(100, 500)
        self.get_service_list_fn = get_service_list_fn
        self.is_leader = is_leader
        self.is_election_running = False
        self.service = {
            'service_id': self.service_id,
            'address': service['Address'],
            'port': service['Port'],
            'is_leader': self.is_leader,
            'election': self.is_election_running
        }
        self.services = []
        self.ongoing_election = False
        self.has_leader = False
        self.election_status_updated = False

        self._lock = False
        self._timeout = random.randint(20, 50)
        self._is_coordinator_timer_set = False
        self._election_message_sent_to_higher_nodes = False
        self._coordinator_message_sent = False
        self.work_thread = work_thread.WorkThread()

        self.master = None
        self._init_sync_services_and_election_thread()

    def become_leader(self):

        higher_services = self._get_higher_services()

        if not self.ongoing_election or self._lock:
            print('Attempting to start the election...')
            print('_________________________')
            if not self.ongoing_election and not self.election_status_updated:
                self._update_election_status()

            if len(higher_services) == 0:
                print('higher node count: 0.')
                self._init_coordinator_message_timer()
            else:
                node_statues = []
                print('...Starting election...', f"higher nodes count {len(higher_services)}")
                for service in higher_services:
                    print(f"Sending Election message to: {service['address']}:{service['port']}")
                    payload = {
                        'service_id': self.service_id
                    }
                    response = requests.post(f"{service['address']}:{service['port']}/election", json=payload)
                    response_json = json.loads(response.content)
                    node_statues.append(response.status_code)
                    print(response.status_code, response_json['data'])

                if self._can_become_coordinator(node_statues):
                    print('_can_become_coordinator', self._can_become_coordinator(node_statues))
                    self._init_coordinator_message_timer()

            self._lock = False

    def init_election(self, wait=True, election_inited_by_node=False):
        if not self.has_leader:
            if wait:
                print(f"waiting to start the election. staring in...", self._timeout)
                print("_________________________")
                election_thread = threading.Timer(self._timeout, self.become_leader)
                election_thread.start()
            elif election_inited_by_node and not self._election_message_sent_to_higher_nodes and not self._coordinator_message_sent:
                print('election init by a node')
                print('*-----------------------*')
                self._lock = True
                self.become_leader()
                self._election_message_sent_to_higher_nodes = True

    def get_service(self):
        return self.service

    def update_service_list(self, service):
        try:
            self.services.index(service)
        except ValueError:
            self.services.append(service)

    def update_leader(self, data):
        self.has_leader = True
        self.master = data
        self.work_thread.init_worker()

    def set_password_range(self, range):
        self.work_thread.set_worker_password_range(range)

    def _send_coordinator_message(self):
        print('**_____________________**')
        print('sending coordinator message')
        self.is_leader = True

        def post_fn(url):
            print(f"sending coordinator message to: {url}")

            response = requests.post(url, json=self.service)
            print(response.status_code)

        urls = [f"{s['address']}:{s['port']}/coordinator" for s in self.services]
        threads = [threading.Thread(target=post_fn, args=(url,)) for url in urls]
        for thread in threads:
            thread.start()

        self._init_master_worker()

    def _init_master_worker(self):
        if self.is_leader:
            self.work_thread.init_master(self.get_worker_list)

    def _sync_services(self):
        service_locations = self.get_service_list_fn()
        self.services = []

        def post_fn(service_location):
            if service_location['Port'] != self.service['port']:
                url = f"{service_location['Address']}:{service_location['Port']}/node-info"
                print(f"Syncing with {url}")
                response = requests.post(url, json=self.service)
                data = json.loads(response.content)['data']
                if data['is_leader']:
                    self.has_leader = True
                self.update_service_list(data)

        threads = [threading.Thread(target=post_fn, args=(service,)) for service in service_locations]
        for thread in threads:
            thread.start()
            # thread.join()

        self._check_leader()
        self._check_election_status()
        self.init_election()

    def _init_coordinator_message_timer(self):
        if not self._is_coordinator_timer_set:
            coordinator_timer = threading.Timer(10, self._send_coordinator_message)
            coordinator_timer.start()
            self._is_coordinator_timer_set = True

    def _init_sync_services_and_election_thread(self):
        print('Sync started...')
        sync_thread = threading.Thread(target=self._sync_services)
        sync_thread.start()

    def _update_election_status(self, is_ongoing=True):

        def post_fn(url):
            print(f"Updating election status in: {url}")
            payload = {
                'ongoing_election': is_ongoing
            }
            response = requests.post(url, json=payload)

        urls = [f"{s['address']}:{s['port']}/ongoing-election-info" for s in self.services]
        threads = [threading.Thread(target=post_fn, args=(url,)) for url in urls]
        for thread in threads:
            thread.start()

        self.election_status_updated = True

    def _check_leader(self):
        if not self.is_leader:
            for service in self.services:
                if service['is_leader']:
                    self.has_leader = True
                    break
        else:
            self.has_leader = True

    def _check_election_status(self):
        if self.is_election_running:
            self.ongoing_election = True
        else:
            for service in self.services:
                if service['election']:
                    self.ongoing_election = True
                    break

    def _get_higher_services(self):
        higher_service_list = []
        for service in self.services:
            if service['service_id'] > self.service_id:
                higher_service_list.append(service)

        return higher_service_list

    def _can_become_coordinator(self, status_list):
        can_become_coordinator = False
        for status in status_list:
            if status != 200:
                can_become_coordinator = True
                break
        return can_become_coordinator

    def get_worker_list(self):
        service_locations = self.get_service_list_fn()
        worker_list = []
        for service_location in service_locations:
            if self.is_leader and service_location['Port'] != self.service['port']:
                worker_list.append(service_location)

        return worker_list
