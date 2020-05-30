from password_cracker import PasswordCracker
from multiprocessing import Process

class Worker:
    def __init__(self):
        self._password_cracker = PasswordCracker()
        print('worker init')

    def set_password_range(self, pw_range):
        print(f"password range updated {pw_range}")
        if pw_range and len(pw_range) == 2:
            self._password_cracker.update_pw_range(pw_range)
            crack_process = Process(target=self.crack_password)
            crack_process.start()
        else:
            raise Exception('Invalid password range')

    def crack_password(self):
        self._password_cracker.crack_password()
