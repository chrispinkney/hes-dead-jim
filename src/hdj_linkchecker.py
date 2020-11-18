# Fixes pytest from screaming at me about not being able to import a local package
try:  # pragma: no cover
    from src import hdj_fileio
except ModuleNotFoundError:  # pragma: no cover
    import hdj_fileio
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import init, Fore, Style
import requests
import re

init()

CLICOLOR = 1

"""
Main checker function.
Receives and checks each link provided by the soup object.
"""


def checker(soup):
    start_time = datetime.now()  # make a timer for fun
    print("Link results:")
    for link in soup.find_all("a"):

        test_link = link.get("href")

        try:
            if "https://" not in test_link and "http://" not in test_link:
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
        except (
            requests.exceptions.MissingSchema,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects,
        ):
            status_check_unknown(test_link)

    print(datetime.now() - start_time)  # end fun timer


"""
URL checker function, runs if CLI args specify a url
"""


def make_soup_object(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup


def single_link_check(url):
    req = requests.get(url)
    return req.status_code


# Various link status code checkers start here.
def status_check_unknown(link):
    if CLICOLOR:
        print(Fore.WHITE + "UNKNOWN LINK: " + link + Style.RESET_ALL)
    else:
        print("UNKNOWN LINK: " + link)


def status_check_200(req, link):
    if CLICOLOR:
        print(
            Fore.GREEN + str(req.status_code) + " SUCCESSFUL: " + link + Style.RESET_ALL
        )
    else:
        print(str(req.status_code) + " SUCCESSFUL: " + link)


def status_check_300(req, link):
    req = requests.head(link, allow_redirects=True)
    if CLICOLOR:
        print(
            Fore.YELLOW
            + "300 REDIRECTED ERROR. "
            + str(len(req.history))
            + " HOP(S) FROM "
            + link
            + " ULTIMATELY ENDED AT "
            + req.url
            + " WITH STATUS CODE: "
            + Fore.WHITE
            + str(req.status_code)
            + Style.RESET_ALL
        )
    else:
        print(
            "300 REDIRECTED ERROR. "
            + str(len(req.history))
            + " HOP(S) FROM "
            + link
            + " ULTIMATELY ENDED AT "
            + req.url
            + " WITH STATUS CODE: "
            + str(req.status_code)
        )


def status_check_400(req, link):
    if CLICOLOR:
        print(
            Fore.RED
            + str(req.status_code)
            + " CLIENT ERROR WITH LINK: "
            + link
            + Style.RESET_ALL
        )
    else:
        print(str(req.status_code) + " CLIENT ERROR WITH LINK: " + link)


def status_check_500(req, link):
    if CLICOLOR:
        print(
            Fore.RED
            + str(req.status_code)
            + " SERVER ERROR WITH LINK: "
            + link
            + Style.RESET_ALL
        )
    else:
        print(str(req.status_code) + " SERVER ERROR WITH LINK: " + link)


# Various link status code checkers end here.


"""
Ignore link checker function, excludes URLs from the checks based on a URL specified in the file provided.
"""


def ignore(ignored_links_file, file_to_check):
    try:
        # open ignored links text file
        with open(ignored_links_file, "r") as f:
            print(f"Reading file: {ignored_links_file}, please wait.")
            ignored_urls_list = regex(f)
            soup = hdj_fileio.file_check_ignored(file_to_check, ignored_urls_list)
            return soup
    except FileNotFoundError:
        print(
            f"The ignored links file specified ({ignored_links_file}) "
            "could not be opened. Please check if your path "
            "is correct or if the file exists."
        )
        raise


"""
Regex for URL checking. This function is used in conjunction with ignore().
"""


def regex(file):
    link_regex = r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"
    urls = []
    for line in file:
        if not line.startswith("#"):
            urls.append(
                re.search(link_regex, line).group(0)
            )  # .group() ensures that the regex will return the entire string if it's matched.
    if urls == []:  # if no urls are found
        print("No URLs could be found inside the specified file. Terminating.")
        quit()
    else:
        return urls


"""
Function to download the last 10 indexed posts
from Telescope's backend (must be running locally)
"""


def telescope():
    baseURL = "http://localhost:3000/posts"  # Specify Telescope's backend's base URL (Can also use Telescope's actual URL)
    res = requests.get(baseURL).json()  # get a response from the base URL's json
    for response in res:  # For each object in the JSON
        id = response.get("id")
        post = f"{baseURL}/{id}"  # Get the ID and create a post URL
        print(f"Testing Post: {post}")
        post = requests.get(
            post, headers={"Accept": "text/html"}
        )  # Create a request from that post's URL
        soup = BeautifulSoup(post.text, "html.parser")
        checker(soup)  # And create a soup object and send it to checker()
