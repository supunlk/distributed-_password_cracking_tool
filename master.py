import math
from string import ascii_lowercase


class Master:

    def __init__(self, get_workers_fn):
        # self.master_node = master
        self.worker_dict = {}
        self.get_worker_fn = get_workers_fn
        self.worker_nodes = None

    def schedule_work(self):

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

    def assign_and_start_work(self, workers=None):
        if workers is None:
            workers = {}
        for worker in workers.values():
            url = f"{worker['Address']}:{worker['Port']}/"
