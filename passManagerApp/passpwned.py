import requests
import hashlib

def checkPassPwned(password):

    sha_password = hashlib.sha1(password.encode()).hexdigest()

    sha_perfix = sha_password[0:5]
    sha_postfix = sha_password[5:].upper()


    url = "https://api.pwnedpasswords.com/range/" + sha_perfix

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    pwned_dict = {}
    pwned_list = response.text.split("\r\n")
    for pwned_pass in pwned_list:
        pwned_hash = pwned_pass.split(":")
        pwned_dict[pwned_hash[0]] = pwned_hash[1]

    if sha_postfix in pwned_dict.keys():
        return format(pwned_dict[sha_postfix])

