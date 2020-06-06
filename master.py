import math
from string import ascii_lowercase
import requests
import threading

class Master:

    def __init__(self, get_workers_fn):
        self.worker_dict = {}
        self.get_worker_fn = get_workers_fn
        self.worker_nodes = None
        self.schedule_work()
        self.password_index = 0

    def schedule_work(self):
        print('scheduling work')
        self.worker_dict = {}
        self.worker_nodes = self.get_worker_fn()

        worker_list_len = len(self.worker_nodes)
        remaining_letters = 26 % worker_list_len
        letter_range = math.floor(26 / worker_list_len)

        _current_cha_position = 0

        for index in range(worker_list_len):
            _worker_node = self.worker_nodes[index]
            self.worker_dict[_worker_node['ID']] = _worker_node
            cha_range = []
            cha_range.append(ascii_lowercase[_current_cha_position] * 6)
            if remaining_letters > 0 and ((_current_cha_position + letter_range) + remaining_letters) == 26:
                cha_range.append(ascii_lowercase[(_current_cha_position + letter_range) + remaining_letters - 1] * 6)
            else:
                cha_range.append(ascii_lowercase[_current_cha_position + (letter_range - 1)] * 6)

            self.worker_dict[_worker_node['ID']]['cha_range'] = cha_range
            _current_cha_position += letter_range

        print('work schedule ready.')
        work_timer = threading.Timer(5, self.assign_and_start_work, args=[self.worker_dict])
        work_timer.start()

    def assign_and_start_work(self, workers=None):
        print('assigning password range')
        if workers is None:
            workers = {}
        for worker in workers.values():
            url = f"{worker['Address']}:{worker['Port']}/worker-instructions"
            requests.post(url, json=worker['cha_range'])


    def read_passwords(self):
        passwords = ['baaaaa', 'agH6Hz', 'XuQjKe', 'ZnZwcy']
        return passwords[self.password_index]

    def compare_passwords(self, data):
        given_password = self.read_passwords()
        print('comparing', given_password, data['password'])
        if data['password'] == given_password:

            print('*********************************')
            print('Given password: ', given_password, 'Password cracked by: ', data['node'], )
            print('*********************************')
            thread = threading.Thread(target=self.stop_cracking, args=[self.worker_dict])
            thread.start()
            self.password_index += 1
            self.schedule_work()
            return True

        return False

    def stop_cracking(self, workers):
        for worker in workers.values():
            url = f"{worker['Address']}:{worker['Port']}/stop-password-cracking"
            requests.post(url, json=worker['cha_range'])