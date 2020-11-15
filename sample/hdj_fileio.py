from bs4 import BeautifulSoup

"""
File checker function, runs if CLI args specify an html file
"""


def file_check(file):
    with open(file, "r") as f:
        soup = BeautifulSoup(f, "html.parser")
        return soup


"""
File checker function, runs if CLI args specify an html file
"""


def file_check_ignored(file, ignored_urls_list):
    try:
        with open(file, "r") as f:  # Open and parse the HTML file
            soup = BeautifulSoup(f, "html.parser")

            print(
                f"Removing links from from: {file}, please wait. This might take a while depending on the file size."
            )

            for link in ignored_urls_list:  # For each link in the file...
                # For each a tag in the HTML file, find an href that matches a link from the ignored links file
                for a in soup.find_all("a", href=f"{link}"):
                    # Destroy the line in the html file that contains the link if found
                    a.decompose()

            return soup  # Send the now parsed object to checker function
    except FileNotFoundError:
        print(
            f"The test file specified ({file}) could not be opened. Please check if your path is correct or if the file exists."
        )
        raise
