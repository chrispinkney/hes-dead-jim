import argparse
import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import init, Fore, Back, Style
init()

# I'm not happy about this, temporary fix until I can figure out a better solution. see: https://click.palletsprojects.com/en/7.x/
if len(sys.argv) == 1:
    print("This program checks for broken links. Please specify -h for help.")
    sys.exit(1)

# Parse the command line arguments
parser = argparse.ArgumentParser(description='See below for optional flags.', prefix_chars='-/')
parser.add_argument('-u', '--url', '-url', metavar='',
                    help='The url to check for broken links. Example: -u http://google.ca')
parser.add_argument('-f', '--file', '-file', metavar='',
                    help='Checks through a specified html file that is located in the current working directory. Example: -f index.html')
parser.add_argument('-v', '--version', '-version', action='store_true',
                    help='Specifies the version')
args = parser.parse_args()


def checker(soup):
    start_time = datetime.now()  # make a timer for fun
    for link in soup.find_all('a'):
        test_link = link.get('href')

        try:
            if 'https://' not in test_link and 'http://' not in test_link:
                print(Fore.WHITE + "UNKNOWN LINK: " + test_link)
            else:
                req = requests.head(test_link)  # using head only instead of body
                if req.status_code in range(200, 226):
                    print(Fore.GREEN + str(req.status_code) + " SUCCESSFUL: " + test_link)
                elif req.status_code in range(300, 308):
                    print(Fore.YELLOW + str(req.status_code) + " REDIRECTED LINK: " + test_link)
                elif req.status_code in range(400, 420):
                    print(Fore.RED + str(req.status_code) + " CLIENT ERROR WITH LINK: " + test_link)
                elif req.status_code in range(500, 599):
                    print(Fore.RED + str(req.status_code) + " SERVER ERROR WITH LINK: " + test_link)
        except:
            print(Fore.WHITE + "UNKNOWN LINK: " + test_link)
    print(datetime.now() - start_time)  # end timer


def url_check():
    # Create a request from the command line arg
    req = requests.get(args.url)

    # Send the req to BS4 for parsing
    soup = BeautifulSoup(req.text, "html.parser")

    # send the soup now parsed object to the checker function
    checker(soup)


def file_check():
    with open(args.file, 'r') as f:
        # create a soup object from the file
        soup = BeautifulSoup(f, "html.parser")

        # send the now parsed soup object to the checker function
        checker(soup)


def version():
    print(Style.BRIGHT + Back.BLUE + Fore.GREEN + "He's Dead, Jim. The Python based link-checker. " + Fore.BLACK + "Version 0.1.04")


if args.url:
    url_check()
if args.file:
    file_check()
if args.version:
    version()