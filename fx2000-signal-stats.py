#!/usr/bin/env python3
import argparse
import hashlib
import os
import re
import requests
import time

# IP address of router interface to login to
router_ip  = "192.168.1.1"

# time to wait between queries in seconds
query_wait = 30

# set the username and password in the environment instead of hard-coding
# abort if not set, you really want these
username = os.environ.get("USER")
password = os.environ.get("PASS")

# URLs to use
urls = { 
         "login": f"http://{router_ip}/login/",
         "post":  f"http://{router_ip}/submitLogin/",
         "diag":  f"http://{router_ip}/diagnostics/",
       }

# ids of fields to scrape from the HTML
diag_fields = [
               "internetStatus4G", 
               "internetStatusTech", 
               "band", 
               "bandwidth", 
               "internetStatusNetworkOperator4G", 
               "internetStatus4gRSSI", 
               "internetStatusSNR" 
              ]

print(f"time,{",".join(diag_fields)}")

# start session
session = requests.Session()

def get_router_token( s: requests.Session, url: str ) -> str:
    """
    query the login page of the router (u) and regex out the gSecureToken value

    return: value of token (str) or None if not found
    """
    try:
        auth_r = session.get(url)
    except requests.exceptions.RequestException as request_err:
        print(f"An error occurred posting authentication information")
        print(f"    '{str(request_err)}'")
        return None

    if auth_r.status_code != 200:
        print(f"Unexpected response from login GET:  ({auth_r.response})")
        return None

    # key off the id of gSecureToken to get the value
    if (m := re.search(r'id="gSecureToken" value="([^"]+)"', auth_r.text)) is not None:
        return m[1]
    else:
        return None

def login_session( s: requests.Session, url: str, password: str, token: str) -> bool:
    """
    using the existing session s, post the SHA1 hash of the password and token
    to the router at url to authenticate the session as admin

    return: True on success, else False
    """

    if len(token) == 0 or len(password) == 0:
        print(f"password length {len(password)} and token length {len(token)} must be greater than 0")
        return False

    # sha1 hash password+token
    sha1 = hashlib.new('sha1')
    sha1.update(f"{password}{token}".encode())

    post_data = { "shaPassword": sha1.hexdigest(), "gSecureToken": token, }
    try:
        post_r = session.post(url, data=post_data)
    except requests.exceptions.RequestException as request_err:
        print(f"An error occurred posting authentication information")
        print(f"    '{str(request_err)}'")
        return False

    if post_r.status_code != 200:
        print(f"Unexpected response from login POST: ({post_r.status_code})")
        return False
    
    return True

def query_page( s: requests.Session, url:str, fields: list[str] ) -> dict[str, str]:
    """
    query url and extract div class id elements in fields using existing 
    (and authenticated) session s. 
    
    return: dict of field:value.
    """

    return_fields = {}
    try: 
        diag_r = session.get(url)
    except requests.exceptions.RequestException as request_err:
        print(f"An error occurred posting authentication information")
        print(f"    '{str(request_err)}'")
        return return_fields

    if diag_r.status_code != 200:
        print(f"Unexpected response from diag GET {diag_r.status_code}")
        return return_fields

    for field in fields:
        reg = r'<div class="input"\s+id="' + field + '">([^<]+)</div>'
        if (m := re.search(reg, diag_r.text)) is not None:
            v =  m[1].strip()
            return_fields[field] = v

    return return_fields

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='fx2000-signal-stats',
                                     description='Report the signal stats from an Inseego FX2000 Wavemaker',)

    parser.add_argument('-l', '--loop', action='store_true', help='Loop over status checks, otherwise one-shot')
    parser.add_argument('-d', '--delay', type=int, default=60, help='Delay between queries when looping')
    args = parser.parse_args()

    # get token to use in password hash
    if (token := get_router_token( s=session, url=urls['login'])) is not None:
    
        # authenticate to access diag status page
        if login_session( s=session, url=urls['post'], password=password, token=token):

            while True:
                # get current stats
                signal_diags = query_page( s=session, url=urls['diag'], fields=diag_fields )
                print(f"{time.time()},", end="")
                for k in diag_fields:
                    v = signal_diags[k] if k in signal_diags else ""
                    print(f"\"{v}\",", end="")
                print()
                
                if not args.loop:
                    break
                else:
                    time.sleep(args.delay)
        else:
            print("Admin login failed, check errors before lockout")
            exit()

