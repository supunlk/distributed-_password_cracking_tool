from password_cracker import PasswordCracker


class Worker:
    def __init__(self):
            self._password_cracker = PasswordCracker()


    def set_password_range(self, pw_range):
        if range and len(pw_range) == 2:
            self._password_cracker.letter_range = pw_range
        else:
            raise Exception('Invalid password range')

    def crack_password(self):
        self._password_cracker.crack_password()
