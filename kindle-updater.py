# Kindle Updater for Kindle Paperwhite 4 (10th gen)
# v2
 
from urllib.request import urlopen # Python 3
from bs4 import BeautifulSoup
import re # regex
from distutils.version import LooseVersion, StrictVersion # porownanie wersji
from colorama import init
from termcolor import colored
# import ctypes 
from win10toast import ToastNotifier
# import folium
# from tkinter import *
import webbrowser

init() # use Colorama to make Termcolor work on Windows
toaster = ToastNotifier() # Windows 10 toast notification

my_version_con = '5.10.1.3'
installation_date = '2018-11-30'

question = input("different than " + my_version_con + "? y/n \n")
if question == "y":
    my_version = input("type version: ")
else:
    my_version = my_version_con

page_url = 'https://www.amazon.com/gp/help/customer/display.html/ref=hp_left_v4_sib?ie=UTF8&nodeId=G54HPVAW86CHYHKS'

page = urlopen(page_url)

soup = BeautifulSoup(page, 'html.parser')

with open("page_scraped.txt", "w") as file:
    file.write(str(soup))

output_file_name = 'page_scraped.txt'  
with open(output_file_name) as output_file:  
    read_file = output_file.read() 
    
current_version = re.search('Software Update( [0-9,.]+)', read_file) # regex pattern search in file

current_version = current_version.group(1) # regex found match

current_version = current_version.strip() # remove any unnecessary chars

update_file_url = re.search('(https:\/\/s3\.amazonaws\.com\/(.*)bin)', read_file) 

update_file_url = update_file_url.group(1)

if LooseVersion(my_version) > LooseVersion(current_version):
    toaster.show_toast("Kindle Updater", "Zainstalowana jest aktualna wersja.", icon_path="icon_ok.ico", duration=5)
    print (colored("zainstalowana jest nowsza wersja", 'green'))
    print ("my version: ", my_version)
    print ("current version: ", current_version)
elif LooseVersion(my_version) == LooseVersion(current_version):
    toaster.show_toast("Kindle Updater", "Zainstalowana jest aktualna wersja.", icon_path="icon_ok.ico", duration=5)
    print (colored("zainstalowana jest najnowsza wersja", 'green'))
    print ("my version: ", my_version)
    print ("current version: ", current_version)
else:
    webbrowser.open(update_file_url)
    toaster.show_toast("Kindle Updater", "Pobieranie aktualizacji: " + current_version, icon_path="icon_download.ico", duration=5) # Windows 10 toast notification
    # ctypes.windll.user32.MessageBoxW(0, "dostepna jest aktualizacja", "Kindle Updater", 0)
    print (colored("dostepna jest aktualizacja", 'red'))
    print ("my version: ", my_version)
    print ("current version: ", current_version)
    
input ("press Enter to continue")