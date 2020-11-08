import hdj_fileio
import hdj_linkchecker
import hdj_util
import argparse
import sys
import threading

"""
Command link argument program control
"""


def main(arguments):
    if arguments.url:
        try:
            soup = hdj_linkchecker.url_check(arguments.url)
            threading.Thread(target=hdj_linkchecker.checker(soup)).start()
        except Exception as e:
            print("Threading exception handled in Main. Details of the Exception: ", e)
            sys.exit(1)
        sys.exit(0)
    elif arguments.file:
        try:
            soup = hdj_fileio.file_check(arguments.file)
            threading.Thread(target=hdj_linkchecker.checker(soup)).start()
        except Exception as e:
            print("Threading exception handled in Main. Details of the Exception: ", e)
            sys.exit(1)
        sys.exit(0)
    elif arguments.telescope:
        try:
            hdj_linkchecker.telescope()
        except Exception as e:
            print("Threading exception handled in Main. Details of the Exception: ", e)
            sys.exit(1)
        sys.exit(0)
    elif arguments.ignore:
        try:
            soup = hdj_linkchecker.ignore(
                arguments.ignore[0][0], arguments.ignore[0][1]
            )
            threading.Thread(target=hdj_linkchecker.checker(soup)).start()
        except Exception as e:
            print("Threading exception handled in Main. Details of the Exception: ", e)
            sys.exit(1)
        sys.exit(0)
    elif args.version:
        hdj_util.version()
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("This program checks for broken links. Please specify -h for help.")
        sys.exit(1)

parser = argparse.ArgumentParser(
    description="See below for optional flags.", prefix_chars="-/"
)
parser.add_argument(
    "-u",
    "--url",
    "-url",
    metavar="",
    help="The url to check for broken links. Example: -u https://google.ca",
)
parser.add_argument(
    "-f",
    "--file",
    "-file",
    metavar="",
    help="Checks through a specified html file that is "
    "located in the current working directory. Example: -f index.html",
)
parser.add_argument(
    "-t",
    "--telescope",
    "-telescope",
    action="store_true",
    help="Function to download the last 10 indexed posts "
    "from Telescope (must be running locally)",
)
parser.add_argument(
    "-i",
    "--ignore",
    "-ignore",
    metavar="",
    nargs=2,
    action="append",
    help="Specify a file filled with links to ignore "
    "when checking a specified page.",
)
parser.add_argument(
    "-v", "--version", "-version", action="store_true", help="Specifies the version"
)
args = parser.parse_args()
main(args)
