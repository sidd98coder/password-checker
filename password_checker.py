import requests
import hashlib
import sys

def request_api_data(initial_chars) :
    url = 'https://api.pwnedpasswords.com/range/' + initial_chars
    res = requests.get(url)
    if res.status_code != 200 :
        raise RuntimeError(f'Error fetching : {res.status_code}. Check the API and try again.')
    return res

def times_password_hacked(hashes, tail_check) :
    hashes_list = (line.split(':') for line in hashes.text.splitlines())
    for hash, hash_times in hashes_list :
        if hash == tail_check :
            return hash_times
    return 0

def pwned_api_check(password) :
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5],sha1password[5:]
    response = request_api_data(first5_char)
    return times_password_hacked(response, tail)



def main(args) :

## taking the password from user to check the number of occurences whether its been used by another user
# by cheking in the haveibeenpwned website.
    for password in args :
        count = pwned_api_check(password)
        print(f'Your password \" {password} \" is hacked {count} times.')
    return 'DONE !!'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))