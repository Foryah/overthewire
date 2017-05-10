import sys
import requests

def write(input_):
    sys.stdout.write(input_)
    sys.stdout.flush()

def check_pass(url, user, key):
    url = "http://{}:{}@{}".format(user, key, url)

    response = requests.get(url)

    if response.status_code == requests.codes.ok:
        return "\nPassword check passed!"
    else:
        return "\nPassword check failed!"


