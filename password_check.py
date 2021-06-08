import hashlib
import sys
import requests


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again.')
    return res


def get_password_leaks_count(hashes, our_hash_tail):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for hash_tail, leak_count in hashes:
        if hash_tail == our_hash_tail:
            return f'Your password is leak "{leak_count}" times. You should change your password!'
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(passwords):
    for password in passwords:
        count = pwned_api_check(password)
        if count:
            print(count)
        else:
            print('Your password is not leak yet.')
    return 'Done!!!'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

