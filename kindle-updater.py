from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

my_version = '5.10.1.3'
installation_date = '2018-11-30'

page_url = 'https://www.amazon.com/gp/help/customer/display.html/ref=hp_left_v4_sib?ie=UTF8&nodeId=G54HPVAW86CHYHKS'

page = urlopen(page_url)

soup = BeautifulSoup(page, 'html.parser')

with open('page_scraped.txt', 'w') as file: 
    file.write(str(soup))

output_file_name = 'page_scraped.txt' 
with open(output_file_name) as output_file: 
    lines = output_file.read()

current_version = re.search('Software Update( [0-9,.]+)', lines)

current_version = current_version.group(1)

current_version = current_version.strip()

print ("current version: ", current_version)
print ('my version: ', my_version)



