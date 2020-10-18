import hdj_fileio
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import init, Fore
import requests
import re
init()

CLICOLOR = 1

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


"""
URL checker function, runs if CLI args specify a url
"""
def url_check(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    #hdj_linkchecker.checker(soup)
    return soup


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
Ignore link checker function, excludes URLs from the checks based on a URL specified in the file provided.
"""
def ignore(ignored_links_file, file_to_check):
    try:
        #open ignored links text file
        with open(ignored_links_file, 'r') as f:
            print(f"Reading file: {ignored_links_file}, please wait.")
            ignored_urls_list = regex(f)
            soup = hdj_fileio.file_check_ignored(file_to_check, ignored_urls_list)
            return soup
    except FileNotFoundError:
        print(f"The ignored links file specified ({ignored_links_file}) could not be opened. Please check if your path is correct or if the file exists.")
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