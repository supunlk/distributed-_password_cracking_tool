from string import ascii_lowercase, digits, ascii_uppercase


class PasswordCracker:
    def __init__(self, compare_fn):
        self.password_range = []
        self.start_password = None
        self.letter_range = None
        self.compare_fn = compare_fn
        print('pw cracker init')
        self.is_password_cracked = False
        self.cracked_by_a_node = False

        self.all_letters = None

    def crack_password(self):
        print('cracking password...')
        crack_pos = 0
        cha_at = 0

        if not self.start_password:
            raise Exception('Start password is required!')

        while not self.is_password_cracked:
            while not self.is_password_cracked and cha_at < len(self.all_letters):
                self.start_password[crack_pos] = self.all_letters[cha_at]
                cha_at += 1
                self.compare(self.start_password)
            crack_pos += 1
            cha_at = 0

            while self.start_password[crack_pos] == self.all_letters[len(self.all_letters) - 1]:
                crack_pos += 1
                next_letter_index = self.get_next_letter_index(crack_pos)
                self.start_password[crack_pos] = self.all_letters[next_letter_index]
                self.start_password[crack_pos - 1] = self.all_letters[cha_at]

            self.start_password[crack_pos] = self.all_letters[self.get_next_letter_index(crack_pos) + 1]

            crack_pos = 0

    def get_next_letter_index(self, crack_pos):
        return self.all_letters.index(self.start_password[crack_pos])

    def compare(self, password):
        if self.cracked_by_a_node:
            self.is_password_cracked = True
        else:
            self.is_password_cracked = self.compare_fn(''.join(password))

    def update_pw_range(self, pw_range):
        self.password_range = pw_range
        self.start_password = list(self.password_range[0])
        self.letter_range = len(self.start_password)

        self.all_letters = ascii_lowercase + digits + ascii_uppercase
