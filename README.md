Script in Python to check if new software version is available for Kindle Paperwhite 4 (or any other model after you change `page_url` in code).

A bit of context why I made it: Kindle doesn't offer an option to check for updates straight from the device so either: 
1. Amazon releases new version and Kindle will automatically download it when connected to network,
2. ^ sometimes it doesn't work, so you may want to download _.bin_ file manually from the website, copy to device and then install it.

Option 2) means every now and then you have to check [Amazon's website](https://www.amazon.com/gp/help/customer/display.html/ref=hp_left_v4_sib?ie=UTF8&nodeId=G54HPVAW86CHYHKS). That gave me an idea to write a script which will automate that. 

Program crawls and scrapes the website, extracts current software version using [regex](https://en.wikipedia.org/wiki/Regular_expression), compares with already installed on my device and if it's newer, then automatically downloads the _.bin_ file. No need to visit a single page 🤓

I used: [win10toast](https://pypi.org/project/win10toast/) for Windows 10 notifications, [colorama](https://pypi.org/project/colorama/) & [termcolor](https://pypi.org/project/termcolor/) for coloring the `print`s in CLI, [distutils](https://docs.python.org/3/distutils/apiref.html#module-distutils.version) to compare versions, [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#) to scrape the website, [urllib](https://docs.python.org/3/library/urllib.request.html) to open the URL for Beautiful Soup.
