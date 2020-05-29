import worker
import master
import requests


class WorkThread:
    def __init__(self):
        self.worker = None
        self.master = None

    def init_worker(self):
        self.worker = worker.Worker()

    def set_worker_password_range(self, pw_range):
        self.worker.set_password_range(pw_range)

    def init_master(self, get_workers_fn):
        self.master = master.Master(get_workers_fn)

    # def check_password_is_cracked(self, password):
    #     payload = {
    #         'password': password
    #     }
    #     requests.post(self.master_url, payload)
