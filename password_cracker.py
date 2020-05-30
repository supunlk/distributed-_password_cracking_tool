from string import ascii_lowercase, digits, ascii_uppercase


class PasswordCracker:
    def __init__(self):
        self.all_letters = ascii_lowercase + digits + ascii_uppercase
        self.password_range = []
        self.start_password = None
        self.letter_range = None
        self.given_password = '09eaaA'
        print('pw cracker init')

    def crack_password(self):
        print('cracking password...')
        crack_pos = 0
        cha_at = 0
        is_password_cracked = True
        if not self.start_password:
            raise Exception('Start password is required!')

        while is_password_cracked:
            while is_password_cracked and cha_at < len(self.all_letters):
                self.start_password[crack_pos] = self.all_letters[cha_at]
                cha_at += 1
                self.compare(self.start_password)
                is_password_cracked = ''.join(self.start_password) != self.given_password

            crack_pos += 1
            cha_at = 0

            while self.start_password[crack_pos] == self.all_letters[len(self.all_letters) - 1]:
                crack_pos += 1
                next_letter_index = self.get_next_letter_index(crack_pos)
                self.start_password[crack_pos] = self.all_letters[next_letter_index]
                self.start_password[crack_pos - 1] = self.all_letters[cha_at]

            self.start_password[crack_pos] = self.all_letters[self.get_next_letter_index(crack_pos) + 1]

            crack_pos = 0
            print('---')

    def get_next_letter_index(self, crack_pos):
        return self.all_letters.index(self.start_password[crack_pos])

    def compare(self, password):
        print(password)

    def update_pw_range(self, pw_range):
        self.password_range = pw_range
        self.start_password = list(self.password_range[0])
        self.letter_range = len(self.start_password)
