# Table of Contents
 - [Releases](#releases)
    1. [He's Dead, Jim (Release 0.1)](#hes-dead-jim-release-01)
		 - [Scope](#scope)
		 - [How It Works](#how-it-works)
		 - [Libraries] (#Libraries)
		 - [Optional Features](#optional-features)
		 - [Usage](#usage)
		 - [TODO](#todo)
		 - [Issues](#issues)
		 - [Contribution](#contribution)
		 - [Licence](#licence)
		 
## RELEASES
### [He's Dead, Jim (Release 0.1)](https://github.com/chrispinkney/OSD600/tree/master/He%27s%20Dead%20Jim)
<p align="center">
  <img src="./assets/hdj/hdj.gif" alt="He's Dead, Jim" width="738">
</p>

#### Scope
For our first project we are tasked with building a command-line tool for finding and reporting dead links (e.g., broken URLs) in a file. Users might use the tool to help locate broken URLs in an HTML page, for example. The tool can be written in any programming language.

#### How It Works
He's Dead, Jim aggregates (a fancy word for saying *grabs*) all href tags on a single page/file and creates get requests for each link on the page. Those requests are then reported back to the user along with the status code and a delightful colour coded message indicating the status of each link.

#### Libraries
 - [Requests](https://requests.readthedocs.io/en/master/)
	 - Requests is an elegant and simple HTTP library for Python, built for human beings.
		 - It grabs the specified URL and saves it for Beautiful Soup to parse and sort.
		 - Requests is also in charge of checking each link.
 - [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
	 - Beautiful Soup is a Python library designed for quick turnaround projects like screen-scraping.
		 - BS4 will grab and store each link from the HTML code of a web page specified (fun fact: this is known as *scraping*).
 - [Argparse](https://github.com/ThomasWaldmann/argparse/)
	 - Argparse makes it easy to write user friendly command line interfaces in Python.
		 - Argparse is in charge of allowing the user to specify which link or file they'd like to run the program on.
		 - Users can specify -f for file-based link checking or -u for url-based link checking. The file must be in the same directory.
 - [Colorama](https://github.com/tartley/colorama)
	 - Colorama is a simple cross-platform program that colors program's output terminal text. It is written in Python.
		 - It colour codes the status of the link returned by Requests.
			 - Green for good, red for bad, grey for unknown.
		 - Colorama is used for one of the optional feature requests for the program.

#### Optional Features
He's Dead Jim features the following optional features:
 - Colourized output. Good URLs are printed in green, bad URLs are printed in red, and unknown URLs in gray.
 - -v can be supplied to the program for current version information.

#### Usage
Install [Python](https://www.python.org/downloads/) on your machine and reboot. Then:

> pip install colorama bs4 argparse requests

> git clone https://github.com/chrispinkney/OSD600.git

> cd OSD600/He's Dead Jim

> python hdj.py

#### TODO
 - ~~Add command line arguments~~
 - ~~Scrape all links in a file~~
 - ~~Scrape all links in a URL~~
 - ~~Add -v for version information~~
 - ~~Colorize output~~
 
#### Issues
Current issues in the projects can be found on the [repo's issues page](https://github.com/chrispinkney/OSD600/issues).

#### Contribution
Feel free to make a Pull Request or Issue regarding and functionality and I'll get to it ASAP.

#### Licence
MIT License - A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.
