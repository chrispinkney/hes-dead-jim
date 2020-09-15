import argparse
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Check for broken links. Use -h for help or --u/--url and specify a URL')
parser.add_argument('--url', metavar='', required=True, help='The url to check for broken links')
args = parser.parse_args()

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