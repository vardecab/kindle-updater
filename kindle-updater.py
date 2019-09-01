# Kindle Updater for Kindle Paperwhite 4 (10th gen)
# v0.9
 
# get What's new
import requests
import lxml

from urllib.request import urlopen # open URLs
from bs4 import BeautifulSoup # BS
import re # regex
from distutils.version import LooseVersion, StrictVersion # versioning
import webbrowser # open browser and download file 

from colorama import init # colored input/output in terminal
from termcolor import colored # colored input/output in terminal

from win10toast import ToastNotifier # Windows 10 notification

import sys # sys.exit()
from sys import platform # check platform (Windows/Linux/macOS)

init()
toaster = ToastNotifier() 

page_url = 'https://www.amazon.com/gp/help/customer/display.html/ref=hp_left_v4_sib?ie=UTF8&nodeId=G54HPVAW86CHYHKS'

try: 
    page = urlopen(page_url)
except: 
    sys.exit("No internet connection. Program exiting...")

output_file_name_software_version = 'data/software_version.txt'  
with open(output_file_name_software_version) as output_file_software_version:  
    read_file_software_version = output_file_software_version.read() 

question_diff_version = input("Version different than " + read_file_software_version + "?\ny/n: ")
if question_diff_version == "y":
    my_version = input("Type your version: ")
    with open("data/software_version.txt", "w") as file:
        file.write(str(my_version))
else:
    my_version = read_file_software_version

soup = BeautifulSoup(page, 'html.parser')

with open("data/page_scraped.html", "w") as file:
    file.write(str(soup))

output_file_name = 'data/page_scraped.html'  
with open(output_file_name) as output_file:  
    read_file = output_file.read() 
    
current_version = re.search('(?<=v2_)(.*)(?=.bin)', read_file) 

current_version = current_version.group(1)

current_version = current_version.strip() 

update_file_url = re.search('(https:\/\/s3\.amazonaws\.com\/(.*)bin)', read_file)

update_file_url = update_file_url.group(1)

if LooseVersion(my_version) > LooseVersion(current_version):
    print (colored("Newer version installed. No updates available.", 'green'))
    if platform == "win32":
        toaster.show_toast("Kindle Updater", "Your version is up to date.", icon_path="images/icon_ok.ico")
elif LooseVersion(my_version) == LooseVersion(current_version):
    print (colored("Newest version installed. No updates available.", 'green'))
    if platform == "win32":
        toaster.show_toast("Kindle Updater", "Your version is up to date.", icon_path="images/icon_ok.ico")
else: # update available
    write_new_version = open("data/software_version.txt", "w")
    write_new_version.write(str(current_version))
    print (colored("Update available: " + current_version, 'red'))
    if platform == "win32":
        toaster.show_toast("Kindle Updater", "Update available: " + current_version, icon_path="images/icon_info.ico")

    r = requests.get(page_url)
    soup = BeautifulSoup(r.content, 'lxml')
    text = [i.text.strip() for i in soup.select('p:has(strong:contains("Here’s what’s new:")), p:has(strong:contains("Here’s what’s new:")) + p + ul li')]
    print(colored('\n'.join(text), 'yellow'))
    text_list = ('\n'.join(text))
    with open("data/whats_new.txt", "w") as file:
        file.write(text_list) 

    question_download = input("Download now?\ny/n: ")
    if question_download == "y":
        print (colored("Downloading update: " + current_version, 'yellow'))
        if platform == "win32":
            toaster.show_toast("Kindle Updater", "Downloading update: " + current_version, icon_path="images/icon_download.ico")
        # print ("my version: ", my_version)
        webbrowser.open(update_file_url)
    
input ("Press Enter to continue...")