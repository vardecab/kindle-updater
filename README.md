# Kindle Updater

![Actively Maintained](https://img.shields.io/badge/Maintenance%20Level-Actively%20Maintained-green.svg)
<br>
![](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-blue)

>Script in Python to check if new software version is available for Kindle Paperwhite 4 (or any other model after you change a couple of variables). Just a simple proof of concept project.

## Modify for other Kindle models

To look for updates for other Kindle models change 2 variables: 
1) update URL in `update_file_url`
2) change selector in `getLatestVersion`

## Context

A bit of context why I made it: Kindle doesn't offer an option to check for updates straight from the device so either: 
1. Amazon releases new version and Kindle will automatically download it when connected to network after ~ 2 months from initial release,
2. ^ sometimes it doesn't work or you don't want to wait, so you may want to download _.bin_ file manually from the website, copy to your device and then install it.

Option 2) means every now and then you have to check [Amazon's website](https://www.amazon.com/gp/help/customer/display.html?nodeId=GKMQC26VQQMM8XSW). That gave me an idea to write a script which will automate that. 

Program crawls and scrapes the website, extracts current software version using [regex](https://en.wikipedia.org/wiki/Regular_expression), compares with already installed on my device (assuming I know version number) and if it's newer, then automatically downloads the _.bin_ file. No need to visit a single page 🤓

## Release History

- 1.2.1: New library used for displaying Windows notifications.
- 1.2: Fixed selector; removed sound from macOS notifications.
- 1.1.2: Fixed icons not working (and changed them).
- 1.1.1: Fix for a bug when launching via [SwiftBar](https://github.com/swiftbar/SwiftBar).
- 1.1.0: Fixed selector so it now works; tweaked a few minor things; added a possibility to open the URL of newest version file from notification.
- 1.0: Re-wrote the script so it works with the updated Amazon website; supports both macOS and Windows; supports notifications on both platforms; added input timeout.

## Versioning

Using [SemVer](http://semver.org/).

## License

![](https://img.shields.io/github/license/vardecab/kindle-updater)
<!-- GNU General Public License v3.0, see [LICENSE.md](https://github.com/vardecab/kindle-updater/blob/master/LICENSE). -->

## Acknowledgements

### Core
- Scraping data with [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#)
- [inputimeout](https://pypi.org/project/inputimeout/)
- Windows notifications done with: [plyer](https://pypi.org/project/plyer/)
- macOS notifications done with: [pync](https://github.com/SeTeM/pync)
- Colored text in the terminal: [colorama](https://pypi.org/project/colorama/)
- Colored text in the terminal: [termcolor](https://pypi.org/project/termcolor/)

### Other
- Icons from [Flaticon](https://www.flaticon.com)
- Icons hosted on [ImgBB](https://imgbb.com)
- .png → .ico conversion with [CloudConvert](https://cloudconvert.com/png-to-ico)

## Contributing

![](https://img.shields.io/github/issues/vardecab/kindle-updater)

If you found a bug or want to propose a feature, feel free to visit [the Issues page](https://github.com/vardecab/kindle-updater/issues).
