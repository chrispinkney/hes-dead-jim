import argparse
import requests
import sys
import threading
import re
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import init, Fore, Back, Style
init()

CLICOLOR = 1


if len(sys.argv) == 1:
    print("This program checks for broken links. Please specify -h for help.")
    sys.exit(1)

parser = argparse.ArgumentParser(description='See below for optional flags.', prefix_chars='-/')
parser.add_argument('-u', '--url', '-url', metavar='',
                    help='The url to check for broken links. Example: -u http://google.ca')
parser.add_argument('-f', '--file', '-file', metavar='',
                    help='Checks through a specified html file that is located in the current working directory. Example: -f index.html')
parser.add_argument('-i', '--ignore', '-ignore', metavar='', nargs=2, action='append',
                    help='Specify a file filled with links to ignore when checking a specified page.')
parser.add_argument('-v', '--version', '-version', action='store_true',
                    help='Specifies the version')
args = parser.parse_args()


"""
Main checker function. Receives and checks each link provided by the soup object.
"""
def checker(soup):
    start_time = datetime.now()  # make a timer for fun
    print(f"Link results:")
    for link in soup.find_all('a'):

        test_link = link.get('href')

        try:
            if 'https://' not in test_link and 'http://' not in test_link:
                status_check_unknown(test_link)
            else:
                req = requests.head(test_link)
                if req.status_code in range(200, 226):
                    status_check_200(req, test_link)
                elif req.status_code in range(300, 308):
                    status_check_300(req, test_link)
                elif req.status_code in range(400, 420):
                    status_check_400(req, test_link)
                else:
                    status_check_500(req, test_link)
        except:
            status_check_unknown(test_link)

    print(datetime.now() - start_time)  # end fun timer


#Various link status code checkers start here.
def status_check_unknown(link):
    if CLICOLOR:
        print(Fore.WHITE + "UNKNOWN LINK: " + link)
    else:
        print("UNKNOWN LINK: " + link)


def status_check_200(req, link):
    if CLICOLOR:
        print(Fore.GREEN + str(req.status_code) + " SUCCESSFUL: " + link)
    else:
        print(str(req.status_code) + " SUCCESSFUL: " + link)


def status_check_300(req, link):
    req = requests.head(link, allow_redirects=True)
    if CLICOLOR:
        print(Fore.YELLOW + "300 REDIRECTED ERROR. " + str(len(
            req.history)) + " HOP(S) FROM " + link + " ULTIMATELY ENDED AT " + req.url + " WITH STATUS CODE: " + Fore.WHITE + str(
            req.status_code))
    else:
        print("300 REDIRECTED ERROR. " + str(len(
            req.history)) + " HOP(S) FROM " + link + " ULTIMATELY ENDED AT " + req.url + " WITH STATUS CODE: " + str(
            req.status_code))


def status_check_400(req, link):
    if CLICOLOR:
        print(Fore.RED + str(req.status_code) + " CLIENT ERROR WITH LINK: " + link)
    else:
        print(str(req.status_code) + " CLIENT ERROR WITH LINK: " + link)


def status_check_500(req, link):
    if CLICOLOR:
        print(Fore.RED + str(req.status_code) + " SERVER ERROR WITH LINK: " + link)
    else:
        print(str(req.status_code) + " SERVER ERROR WITH LINK: " + link)
#Various link status code checkers end here.


"""
URL checker function, runs if CLI args specify a url
"""
def url_check():
    req = requests.get(args.url)
    soup = BeautifulSoup(req.text, "html.parser")
    checker(soup)


"""
File checker function, runs if CLI args specify an html file
"""
def file_check():
    with open(args.file, 'r') as f:
        soup = BeautifulSoup(f, "html.parser")
        checker(soup)


"""
File checker function, runs if CLI args specify an html file
"""
def file_check_ignored(ignored_urls_list):
    try:
        with open(args.ignore[0][1], 'r') as f:  # Open and parse the HTML file
            soup = BeautifulSoup(f, "html.parser")

            print(f"Removing links from from: {args.ignore[0][1]}, please wait. This might take a while depending on the file size.")

            for link in ignored_urls_list:  # For each link in the file...
                    for a in soup.find_all('a', href=f"{link}"):  # For each a tag in the HTML file, find an href that matches a link from the ignored links file
                        a.decompose()  # Destroy the line in the html file that contains the link if found

            checker(soup)  # Send the now parsed object to checker function
    except FileNotFoundError:
        print(f"The test file specified ({args.ignore[0][1]}) could not be opened. Please check if your path is correct or if the file exists.")
        quit()


"""
Ignore link checker function, excludes URLs from the checks based on a URL specified in the file provided.
"""
def ignore():
    try:
        with open(args.ignore[0][0], 'r') as f:
            print(f"Reading file: {args.ignore[0][0]}, please wait.")
            urls = regex(f)
            file_check_ignored(urls)
    except FileNotFoundError:
        print(f"The ignored links file specified ({args.ignore[0][0]}) could not be opened. Please check if your path is correct or if the file exists.")
        quit()


"""
Regex for URL checking. This function is used in conjuuction with ignore().
"""
def regex(file):
    # r = r"(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
    # r = r"(https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+)"
    link_regex = r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"
    urls = []
    for line in file:
        if not line.startswith("#"):
            urls.append(re.search(link_regex, line).group(0)) #.group() ensures that the regex will return the entire string if it's matched.
    if urls == []:  # if no urls are found
        print(f"No URLs could be found inside the specified file. Terminating.")
        quit()
    else:
        return urls


"""
Prints out the version of the software
"""
def version():
    print(Style.BRIGHT + Back.BLUE + Fore.GREEN + "He's Dead, Jim. The Python based link-checker. " + Fore.BLACK + "Version 0.1.04")


"""
Command link argument program control
"""
if args.url:
    try:
        threading.Thread(target=url_check()).start()
    except:
        sys.exit(1)
    sys.exit(0)
elif args.file:
    try:
        threading.Thread(target=file_check()).start()
    except:
        sys.exit(1)
    sys.exit(0)
elif args.ignore:
    try:
        threading.Thread(target=ignore()).start()
    except:
        sys.exit(1)
    sys.exit(0)
elif args.version:
    version()
