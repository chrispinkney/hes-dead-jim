import argparse
import requests
import sys
from bs4 import BeautifulSoup
from colorama import init, Fore
init()

# I'm not happy about this, temporary fix until I can figure out a better solution. see: https://click.palletsprojects.com/en/7.x/
if len(sys.argv) == 1:
    print("This program checks for broken links. Please specify -h for help.")
    sys.exit(1)

# Parse the command line arguments
parser = argparse.ArgumentParser(description='See below for optional flags.')
parser.add_argument('-u', '--url', '-url', metavar='',
                    help='The url to check for broken links. Example: -u http://google.ca')
parser.add_argument('-f', '--file', '-file', metavar='',
                    help='Checks through a specified html file that is located in the current working directory. Example: -f index.html')
args = parser.parse_args()


def checker(soup):
    for link in soup.find_all('a'):
        l = link.get('href')

        if 'https://' not in l and 'http://' not in l:
            print(Fore.RED + "UNKNOWN LINK: " + l)
        else:
            req = requests.get(l)
            if req.status_code in range(200, 226):
                print(Fore.GREEN + str(req.status_code) + " SUCCESSFUL: " + l)
            elif req.status_code in range(300, 308):
                print(Fore.GREY + str(req.status_code) + " REDIRECTED LINK: " + l)
            elif req.status_code in range(400, 420):
                print(Fore.RED + str(req.status_code) + " CLIENT ERROR WITH LINK: " + l)
            elif req.status_code in range(500, 599):
                print(Fore.RED + str(req.status_code) + " SERVER ERROR WITH LINK: " + l)


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


if args.url:
    url_check()
if args.file:
    file_check()
