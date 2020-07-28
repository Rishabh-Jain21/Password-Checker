import requests
import hashlib


def request_api_data(query_char):
    # k Anonimity is used here no need to give complete password to url
    url = 'https://api.pwnedpasswords.com/range/'+query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error Fetching: {res.status_code}, check API and try again')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[0:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main():
    seperator = input(
        "Enter symbol(s) which will act as seperator between passwords: ")
    if seperator is None or seperator.isalnum():
        print("Invalid Sepetator")
        main()
    else:
        check = input(
            "Enter the passwords you want to check ").split(seperator)
        for password in check:
            count = pwned_api_check(password)
            if count:
                print(
                    f'{password} was found {count} times ')
            else:
                print(f'{password} was NOT found.')


main()
