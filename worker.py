from password_cracker import PasswordCracker
from multiprocessing import Process
import threading
import time


class Worker:
    def __init__(self, compare_fn):
        self._password_cracker = PasswordCracker(self.compare_password_callback)
        self.compare_fn = compare_fn
        print('worker init')

    def set_password_range(self, pw_range):
        print(f"password range updated {pw_range}")
        if pw_range and len(pw_range) == 2:
            self._password_cracker.update_pw_range(pw_range)
            crack_process = threading.Thread(target=self.crack_password)
            crack_process.start()
        else:
            raise Exception('Invalid password range')

    def crack_password(self):
        self._password_cracker.crack_password()
        self._password_cracker.cracked_by_a_node = False
        self._password_cracker.is_password_cracked = False

    def compare_password_callback(self, password):
        print(password)
        return self.compare_fn(password)

    def stop_password_cracking(self):
        self._password_cracker.cracked_by_a_node = True

