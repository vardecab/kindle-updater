# ==================================== #
#            Kindle Updater            #
#          Kindle Paperwhite 4         #
#               10th gen               #
#                v1.1.0                #
# ==================================== #

# ------------ import libs ----------- #

from urllib.request import urlopen # open URLs
from bs4 import BeautifulSoup # BeautifulSoup; parsing HTML
import re # regex; extract substrings
from distutils.version import LooseVersion, StrictVersion # versioning; compare versions // TODO: it's going to be removed in Python 3.12 → find alternative 
import webbrowser # open browser and download file 
import sys # sys.exit()
from sys import platform # check platform (Windows/macOS)
if platform == 'win32': # Windows
    from colorama import init # colored input/output in terminal
    from win10toast_click import ToastNotifier # Windows 10 notifications
    toaster = ToastNotifier() # initialize win10toast
elif platform == 'darwin': # macOS
    from termcolor import colored # colored input/output in terminal
    import pync # macOS notifications 
import time # calculate script's run time
from inputimeout import inputimeout, TimeoutOccurred # input timeout: https://pypi.org/project/inputimeout/

# --------- fix opening page --------- #

import ssl # certificate issue fix: https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate
import certifi # certificate issue fix: https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate
from urllib.request import urlopen, Request # open URLs; Request to fix blocked user-agent: https://stackoverflow.com/questions/16627227/

# --------- start + run time --------- #

start_time = time.time() # run time start
print("Starting...")

# ------------- open URL ------------- #

page_url = 'https://www.amazon.com/gp/help/customer/display.html?nodeId=G54HPVAW86CHYHKS' # "Kindle E-Reader Software Updates" page

# try to open the URL, if fails then close the program
try: 
    print('Opening URL...')

    # *NOTE: fix for 503 error
    request = Request(page_url, headers={'User-Agent': 'XYZ/3.0'}) # using different agent to not get blocked
    page = urlopen(request, timeout=5, context=ssl.create_default_context(cafile=certifi.where()))
except: 
    sys.exit("No internet connection. Program exiting...")

# --------- get software version --------- #

# if stored locally
software_version_local_file = "data/software_version.txt" # local file to store software version
print('Reading local file to get software version...')

try: 
    with open(software_version_local_file) as software_version_local_file: # open local file...
        read_software_version_local_file = software_version_local_file.read() # ... and read it
except FileNotFoundError:
    print("File not found. Looks like it's a first launch of this script. Using default version '5.0'.") 
    read_software_version_local_file = '5.0'
    with open(software_version_local_file, "w", encoding="utf-8") as saveVersion:
        print('Saving file...')
        saveVersion.write(read_software_version_local_file) # save file locally

# get software version from user
timeout_time = 5 # seconds to wait 
print(f'Script will wait {timeout_time} seconds for the input and then will continue with a default value.')

try:
    question_diff_version = inputimeout(prompt="Version different than " + read_software_version_local_file + "?\ny/n: ", timeout=timeout_time) # check if user has different version
    try:
        if question_diff_version == "y":
            my_version = inputimeout(prompt="Type your version: ", timeout=timeout_time)
            with open("data/software_version.txt", "w") as file: # open file...
                file.write(str(my_version)) # ... and write software version
        else:
            my_version = read_software_version_local_file # if "n" then what's in the file = existing software version
    except TimeoutOccurred:
        my_version = read_software_version_local_file
        print(f"Time ran out. Selecting default value from file: {my_version}")
except TimeoutOccurred:
    print(f"Time ran out. Selecting current version, {read_software_version_local_file}.")
    my_version = read_software_version_local_file 

# ---------- scrape website ---------- #

soup = BeautifulSoup(page, 'html.parser') # parse the page

# *NOTE: change if you want a different model
getLatestVersion = soup.select("#GUID-E5C7ABBF-B934-4B95-9B7A-872D0A77CD4B__GUID-79E9B5FE-EFF4-4D5F-91FD-358D14A04FC7") # find Paperwhite on the list
getLatestVersion = str(getLatestVersion) # convert to string
getLatestVersion = re.search("(?<=>)(.*)(?=<)", getLatestVersion) # extract software version from <span> tag 
getLatestVersion = getLatestVersion.group() # returns the part of the string where there was a match
getLatestVersion = getLatestVersion.strip() # remove space " " from the beginning of the string 

# ---------- open update URL --------- #

# *NOTE: change if you want a different model

# for macOS
update_file_url = 'https://www.amazon.com/update_Kindle_Paperwhite_10th_Gen'

# for Windows
def open_url():
    try: 
        webbrowser.open_new(update_file_url)
        print('Opening URL...') # status
    except: 
        print('Failed to open URL. Unsupported variable type.')

# --------- compare versions --------- #

latest_version = getLatestVersion

if LooseVersion(my_version) > LooseVersion(latest_version):
    print (colored("Newer version is installed. No updates available.", 'green')) # green output
    if platform == "win32":
        toaster.show_toast("Kindle Updater", "Your version is up to date.", icon_path="icons/icon_ok.ico")
    elif platform == 'darwin':
        pync.notify(f'Your version is up to date.', title='Kindle Updater', contentImage="https://image.flaticon.com/icons/png/512/3699/3699516.png", sound="Funk") # appIcon="" doesn't work, using contentImage instead)
elif LooseVersion(my_version) == LooseVersion(latest_version):
    print (colored("The newest version is installed. No updates available.", 'green')) # green output
    if platform == "win32":
        toaster.show_toast("Kindle Updater", "Your version is up to date.", icon_path="icons/icon_ok.ico")
    elif platform == 'darwin':
        pync.notify(f'Your version is up to date.', title='Kindle Updater', contentImage="https://image.flaticon.com/icons/png/512/3699/3699516.png", sound="Funk") # appIcon="" doesn't work, using contentImage instead)
else: # update available
    print (colored("Update available: " + latest_version, 'red')) # red output
    if platform == "win32":
        toaster.show_toast("Kindle Updater", "Update available: " + latest_version, icon_path="icons/icon_info.ico", callback_on_click=open_url)
    elif platform == 'darwin':
        pync.notify(f'Update available: {latest_version}', title='Kindle Updater', contentImage="https://image.flaticon.com/icons/png/512/594/594801.png", sound="Funk", open=update_file_url) # appIcon="" doesn't work, using contentImage instead)

    # ---------- download update --------- #
    
    timeout_time = 30
    try:
        question_download_update = inputimeout(prompt="Download now?\ny/n: ", timeout=timeout_time)
        if question_download_update == "y":
            print (colored("Downloading update: " + latest_version, 'yellow')) # yellow output
            if platform == "win32":
                toaster.show_toast("Kindle Updater", "Downloading update: " + latest_version, icon_path="icons/icon_download.ico")
            elif platform == 'darwin':
                pync.notify(f'Downloading update: {latest_version}', title='Kindle Updater', contentImage="https://image.flaticon.com/icons/png/512/4403/4403171.png", sound="Funk") # appIcon="" doesn't work, using contentImage instead)
            webbrowser.open(update_file_url) # open `.bin` URL in browser and download the update
            
            # ---- save new version to a file ---- #
            
            write_new_version_to_local_file = open("data/software_version.txt", "w") # open file...
            write_new_version_to_local_file.write(latest_version) # ... and write latest version there so file is up-to-date for checks in future
            
        else:
            print('Ok, not downloading.')
    except TimeoutOccurred:
        print("Time ran out. Not downloading.")
    
# input ("Press Enter to close the script >>>") # wait for input = window won't close

# ------------- run time ------------- #

end_time = time.time() # run time end 
run_time = round(end_time-start_time,2)
print("Script run time:", run_time, "seconds. That's", round(run_time/60,2), "minutes.")