# Kindle Updater for Kindle Paperwhite 4 (10th gen)
# v4
 
import webbrowser 
import re
from urllib.request import urlopen 
from bs4 import BeautifulSoup
from distutils.version import LooseVersion, StrictVersion 
from colorama import init
from termcolor import colored
from win10toast import ToastNotifier

init()
toaster = ToastNotifier() 

output_file_name_software_version = 'software_version.txt'  
with open(output_file_name_software_version) as output_file_software_version:  
    read_file_software_version = output_file_software_version.read() 

question_diff_version = input("Version different than " + read_file_software_version + "?\ny/n: ")
if question_diff_version == "y":
    my_version = input("Type your version: ")
    with open("software_version.txt", "w") as file:
        file.write(str(my_version))
else:
    my_version = read_file_software_version

page_url = 'https://www.amazon.com/gp/help/customer/display.html/ref=hp_left_v4_sib?ie=UTF8&nodeId=G54HPVAW86CHYHKS'

page = urlopen(page_url)

soup = BeautifulSoup(page, 'html.parser')

with open("page_scraped.txt", "w") as file:
    file.write(str(soup))

output_file_name = 'page_scraped.txt'  
with open(output_file_name) as output_file:  
    read_file = output_file.read() 
    
current_version = re.search('(?<=v2_)(.*)(?=.bin)', read_file)

current_version = current_version.group(1) 

current_version = current_version.strip() 

update_file_url = re.search('(https:\/\/s3\.amazonaws\.com\/(.*)bin)', read_file) 

update_file_url = update_file_url.group(1)

if LooseVersion(my_version) > LooseVersion(current_version):
    print (colored("Newer version installed. No updates available.", 'green'))
    toaster.show_toast("Kindle Updater", "Your version is up to date.", icon_path="icon_ok.ico")
elif LooseVersion(my_version) == LooseVersion(current_version):
    print (colored("Newest version installed. No updates available.", 'green'))
    toaster.show_toast("Kindle Updater", "Your version is up to date.", icon_path="icon_ok.ico")
else:
    print (colored("Update available: " + current_version, 'red'))
    toaster.show_toast("Kindle Updater", "Update available: " + current_version, icon_path="icon_info.ico")
    question_download = input("Download now?\ny/n: ")
    if question_download == "y":
        print (colored("Downloading update: " + current_version, 'yellow'))
        toaster.show_toast("Kindle Updater", "Downloading update: " + current_version, icon_path="icon_download.ico")
        print ("my version: ", my_version)
        webbrowser.open(update_file_url)
    
input ("Press Enter to continue...")
