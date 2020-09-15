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
        # try to make a request, if it fails just throw unknown link
        # but req.status_code == 200 might be reached before the try is excuted (i.e. a bad link is sent first). options?
        try:
            req = requests.get(l)
        except requests.exceptions.MissingSchema:
            pass

        # if the link doesn't begin with a valid schema, throw unknown link. "/t/contact_us" from youtube.com is not a valid link.
        if 'https://' not in l:
            print(Fore.RED + "UNKNOWN LINK: " + l)
        elif req.status_code == 200:
            #print("entered here")
            print(Fore.GREEN + "SUCCESS LINK: " + l)
        elif req.status_code == 300:
            print(Fore.GREY + "300 REDIRECTED LINK: " + l)
        elif req.status_code == 400 or req.status_code == 404:
            print(Fore.RED + "400 ERROR LINK: " + l)
        elif req.status_code == 500:
            print(Fore.RED + "500 ERROR LINK: " + l)


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
