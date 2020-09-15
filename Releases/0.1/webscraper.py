import argparse
import requests
import sys
from bs4 import BeautifulSoup

# I'm not happy about this, temporary fix until I can figure out a better solution.
if len(sys.argv) == 1:
    print("This program checks for broken links. Please specify a webpage with --url <url to check> or -h for help.")
    sys.exit(1)

# Parse the command line arguments
parser = argparse.ArgumentParser(description='See below for optional flags.')
parser.add_argument('-u', '--url', metavar='', required=True, help='The url to check for broken links (must start with http://).')
parser.add_argument('-f', '--file', metavar='', help='Checks through a specified html file (not yet implemented.)')
args = parser.parse_args()

def url_check(url):
    # Create a request from the command line arg
    req = requests.get(args.url)

    # Send the req to BS4 for parsing
    soup = BeautifulSoup(req.text, "html.parser")

    # Finds all href tags in the parsed request and checks if broken
    for a in soup.find_all(href=True):
        if (req.status_code == 200):
            print(f"SUCCESSFUL LINK: {a['href']}")
        elif (req.status_code == 300):
            print(f"REDIRECTED LINK: {a['href']}")
        elif (req.status_code == 400 or req.status_code == 404):
            print(f"DEAD LINK (CLIENT ERROR): {a['href']}")
        elif (req.status_code == 500):
            print(f"DEAD LINK (SERVER ERROR): {a['href']}")
        else: 
            print(f"UNKNOWN LINK: {a['href']}")

url_check(args)