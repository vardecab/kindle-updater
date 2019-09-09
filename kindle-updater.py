# Kindle Updater for Kindle Paperwhite 4 (10th gen)
# v0.10
 
import requests # get "What's new"
import lxml # process HTML; get "What's new"

from urllib.request import urlopen # open URLs
from bs4 import BeautifulSoup # BeautifulSoup; parsing HTML
import re # regex; extract substrings
from distutils.version import LooseVersion, StrictVersion # versioning; compare versions
import webbrowser # open browser and download file 

from colorama import init # colored input/output in terminal
from termcolor import colored # colored input/output in terminal

from win10toast import ToastNotifier # Windows 10 notifications

import sys # sys.exit()
from sys import platform # check platform (Windows/Linux/macOS)

toaster = ToastNotifier() # initialize win10toast

model_page_url = 'https://www.amazon.com/gp/help/customer/display.html/ref=hp_left_v4_sib?ie=UTF8&nodeId=G54HPVAW86CHYHKS' # "Kindle Paperwhite (10th Generation) Software Updates" page

# try to open the URL, if fails then close the program
try: 
    page = urlopen(model_page_url)
except: 
    sys.exit("No internet connection. Program exiting...")

software_version_local_file = 'data/software_version.txt' # local file to store software version
with open(software_version_local_file) as software_version_local_file: # open file...
    read_software_version_local_file = software_version_local_file.read() # ... and read it

question_diff_version = input("Version different than " + read_software_version_local_file + "?\ny/n: ") # check if user has different version
if question_diff_version == "y":
    my_version = input("Type your version: ")
    with open("data/software_version.txt", "w") as file: # open file...
        file.write(str(my_version)) # ... and write software version
else:
    my_version = read_software_version_local_file # if "n" then what's in the file = existing software version

soup = str(BeautifulSoup(page, 'html.parser')) # parse the page
    
latest_version = re.search('(?<=v2_)(.*)(?=.bin)', soup) # regex; find latest software version on the page

latest_version = latest_version.group(1) # regex; returns the substring that was matched by the `re`

latest_version = latest_version.strip() # returns a copy of the string with both leading and trailing characters removed

update_file_url = re.search('(https:\/\/s3\.amazonaws\.com\/(.*)bin)', soup) # find `.bin` update file on the page

update_file_url = update_file_url.group(1) # regex; returns the substring that was matched by the `re`

# compare versions:
if LooseVersion(my_version) > LooseVersion(latest_version):
    print (colored("Newer version installed. No updates available.", 'green')) # green output
    if platform == "win32":
        toaster.show_toast("Kindle Updater", "Your version is up to date.", icon_path="images/icon_ok.ico")
elif LooseVersion(my_version) == LooseVersion(latest_version):
    print (colored("Newest version installed. No updates available.", 'green')) # green output
    if platform == "win32":
        toaster.show_toast("Kindle Updater", "Your version is up to date.", icon_path="images/icon_ok.ico")
else: # update available
    write_new_version_to_local_file = open("data/software_version.txt", "w") # open file...
    write_new_version_to_local_file.write(str(latest_version)) # ... and write latest version there so file is up-to-date for checks in future
    print (colored("Update available: " + latest_version, 'red')) # red output
    if platform == "win32":
        toaster.show_toast("Kindle Updater", "Update available: " + latest_version, icon_path="images/icon_info.ico")

    # "What's new" logic:
    r = requests.get(model_page_url) # get the page...
    soup = BeautifulSoup(r.content, 'lxml') # ... and parse it
    text = [i.text.strip() for i in soup.select('p:has(strong:contains("Here’s what’s new:")), p:has(strong:contains("Here’s what’s new:")) + p + ul li')] # find every "What's new" element on the page and have it in a list
    print(colored('\n'.join(text), 'yellow')) # nice & clean line by line (yellow) output instead of a list 

    # download update:
    question_download_update = input("Download now?\ny/n: ")
    if question_download_update == "y":
        print (colored("Downloading update: " + latest_version, 'yellow')) # yellow output
        if platform == "win32":
            toaster.show_toast("Kindle Updater", "Downloading update: " + latest_version, icon_path="images/icon_download.ico")
        webbrowser.open(update_file_url) # open `.bin` URL in browser and download the update
    
input ("Press Enter to continue...") # wait for input = window won't close