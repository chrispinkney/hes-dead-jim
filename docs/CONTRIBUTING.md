# Welcome

Welcome to He's Dead, Jim! A personal project created and tweaked over the course of 4 months as part of Seneca College's Open Source Development(OSD600) course which I took during Winter 2020.

Here you'll find setup and various information regarding contribution to this project.

See [usage](https://github.com/chrispinkney/He-s-Dead-Jim/blob/master/docs/README.md#usage) for more information in installed packages.

# Configuration

The following section contains information about workspace configuration regarding code formatting and linting used in this project.

The project was developed using PyCharm:

- If opened in PyCharm, the `.idea` profile should be loaded automatically and [File Watchers](https://plugins.jetbrains.com/plugin/7177-file-watchers) should be configured.
  If using PyCharm please ensure the File Watchers is installed to your editor.

## Code Formatting

HDJ utilizes the Black code formatter (which is installed with the project requirements, or globally with `python -m pip install black`).

Please take care to run the following lines prior to any PRs being made:

> cd He-s-Dead-Jim

> black src/hdj.py

to format a specific file, or

> black src

to run the code formatter on the entire `src` directory.

<u>However, please note that upon any PR made to this repository, GitHub Actions checks if the code was formatted correctly using Black.</u>

Note: If you'd like to set up PyCharm to run the code formatter automatically, [please see the official documentation for support](https://black.readthedocs.io/en/stable/editor_integration.html#pycharm-intellij-idea).

## Linting

HDJ utilizes the Flake8 linter (which is installed with the project requirements, or globally with `python -m pip install flake8`).

Please take care to run the following lines prior to any PRs being made, and fix and warnings/errors accordingly (where applicable):

> cd He-s-Dead-Jim

> flake8 src/hdj.py

to display linting results on a specific file, or

> flake8 src

to run the linter on the entire `src` directory.

<u>However, please note that upon any PR made to this repository, GitHub Actions checks if the code was formatted correctly using Black.</u>

If you'd like to set up PyCharm to run the code formatter automatically, [I found this helpful guide on how to do it](https://tirinox.ru/flake8-pycharm) (Note: _It's in Russian but was easy enough to follow along with._)

See also `.flake8` for the project's default flake8 configuration.

## Testing

HDJ utilizes various tests using [Pytest](https://docs.pytest.org/en/latest/). The tests (and testing files) are stored in `./tests`, and as such please ensure that all test files go in this directory. Test filenames must begin with the prefix `text_` in order to be found and ran by pytest. Please add functions to the respective test file, e.g. tests for `hdj_linkchecker.py` go in the `test_hdj_linkchecker.py` test file.

To run pytest locally using all test files, simply execute `pytest` in `\He-s-Dead-Jim`.

To run pytest locally on a specific test file, simply execute `pytest -vv tests/test_file_name.py::test_specific_function` in `\He-s-Dead-Jim`.

To run a testing coverage report (to look for untested code lines in the project), simply execute `pytest --cov-report term-missing --cov=sample tests/` in `\He-s-Dead-Jim`.

<u>However, please note that upon any PR made to this repository, GitHub Actions checks all code commited using the `pytest` command to ensure they pass the bare minimum tests.</u>

## Libraries Used in HDJ

- [Requests](https://requests.readthedocs.io/en/master/)
  - Requests is an elegant and simple HTTP library for Python, built for human beings.
    - It grabs the specified URL and saves it for Beautiful Soup to parse and sort.
    - Requests is also in charge of checking each link.
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
  - Beautiful Soup is a Python library designed for quick turnaround projects like screen-scraping.
    - BS4 will grab and store each link from the HTML code of a web page specified (fun fact: this is known as _scraping_).
- [Argparse](https://github.com/ThomasWaldmann/argparse/)
  - Argparse makes it easy to write user friendly command line interfaces in Python.
    - Argparse is in charge of allowing the user to specify which link or file they'd like to run the program on.
    - Users can specify -f for file-based link checking or -u for url-based link checking. The file must be in the same directory.
- [Colorama](https://github.com/tartley/colorama)

  - Colorama is a simple cross-platform program that colors program's output terminal text. It is written in Python.
    - It colour codes the status of the link returned by Requests.
      - Green for good, red for bad, grey for unknown.
    - Colorama is used for one of the optional feature requests for the program.

- Various other libraries unrelated to the main program: Black/Flake8/pre-commit/pytest.
