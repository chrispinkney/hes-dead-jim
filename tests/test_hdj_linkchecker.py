import src.hdj_linkchecker as lc
import requests
import pytest


def test_get_request_200(monkeypatch):
    """
    Monkeypatches a version of hdj_linkchecker.py's single_link_check() function,
    suchthat the request is always 200 for a given link.
    """

    # Create a mocked object with an http status_code of 200.
    class MockResponse:
        def __init__(self):
            self.status_code = 200

    # Serve the object when called using a monkeypatch
    def mock_get(url):
        return MockResponse()

    # Create a monkeypatch fixture
    monkeypatch.setattr(requests, "get", mock_get)

    assert lc.single_link_check("https://google.ca") == 200


def test_get_request_404(monkeypatch):
    """
    Monkeypatches a version of hdj_linkchecker.py's single_link_check() function,
    suchthat the request is always 404 for a given link.
    """

    # Create a mocked object with an http status_code of 404.
    class MockResponse:
        def __init__(self):
            self.status_code = 404

    # Serve the object when called using a monkeypatch
    def mock_get(url):
        return MockResponse()

    # Create a monkeypatch fixture
    monkeypatch.setattr(requests, "get", mock_get)

    assert lc.single_link_check("https://google.ca") == 404


# Test that ensures the links that are being ignored are removed from the html file
def test_ignore():
    output = '<!DOCTYPE html>\n\n<html>\n<head>\n<title>Header</title>\n<meta charset="utf-8"/>\n</head>\n<body>\n<a href="https://github.com/chrispinkney"> Working link here </a>\n\n</body>\n</html>\n'
    soup = lc.ignore("tests/ignore-urls.txt", "tests/test1.html")
    assert str(soup) == output


# Tests that ignore properly freaks out when provided a bad txt file
def test_ignore_BadTxtFile():
    with pytest.raises(FileNotFoundError):
        lc.ignore("", "tests/test1.html")


# Tests that ignore properly freaks out when provided a bad HTML file
def test_ignore_BadHTMLFile():
    with pytest.raises(FileNotFoundError):
        lc.ignore("tests/ignore-urls.txt", "")


# Tests that ignore properly freaks out when provided not one, but TWO bad files
def test_ignore_BadBothFile():
    with pytest.raises(FileNotFoundError):
        lc.ignore("", "")


# Tests make_soup_object to ensure that it properly returns proper html
def test_make_soup_object(monkeypatch):
    # Create a mocked object with an http status_code of 200.
    class MockResponse:
        def __init__(self):
            self.url = "https://telescope.cdot.systems/"
            self.status_code = 200
            self.text = "<p>Oh good, more blogs.</p>"

    # Serve the object when called using a monkeypatch
    def mock_get(url):
        return MockResponse()

    # Create a monkeypatch fixture
    monkeypatch.setattr(requests, "get", mock_get)

    soup = lc.make_soup_object("https://telescope.cdot.systems/")

    assert str(soup) == "<p>Oh good, more blogs.</p>"


# Tests that status_check_unknown() still returns coloured output
def test_status_check_unknown(capsys):
    expected = "\x1b[37mUNKNOWN LINK: https://google.ca\x1b[0m\n"
    lc.status_check_unknown("https://google.ca")
    captured = capsys.readouterr()
    assert captured.out == expected


# Tests that status_check_200() still returns coloured output
def test_status_check_200(capsys, monkeypatch):
    class MockResponse:
        def __init__(self):
            self.status_code = 200

    mock = MockResponse()

    expected = "\x1b[32m200 SUCCESSFUL: https://google.ca\x1b[0m\n"
    lc.status_check_200(mock, "https://google.ca")
    captured = capsys.readouterr()

    assert captured.out == expected


# Tests that status_check_300() still returns coloured output
def test_status_check_300(capsys):
    class MockResponse:
        def __init__(self):
            self.status_code = 300

    mock = MockResponse()

    expected = "\x1b[33m300 REDIRECTED ERROR. 1 HOP(S) FROM https://google.ca ULTIMATELY ENDED AT https://www.google.ca/ WITH STATUS CODE: \x1b[37m200\x1b[0m\n"
    lc.status_check_300(mock, "https://google.ca")
    captured = capsys.readouterr()
    assert captured.out == expected


# Tests that status_check_400() still returns coloured output
def test_status_check_400(capsys):
    class MockResponse:
        def __init__(self):
            self.status_code = 400

    mock = MockResponse()

    expected = "\x1b[31m400 CLIENT ERROR WITH LINK: https://google.ca\x1b[0m\n"
    lc.status_check_400(mock, "https://google.ca")
    captured = capsys.readouterr()

    assert captured.out == expected


# Tests that status_check_500() still returns coloured output
def test_status_check_500(capsys):
    class MockResponse:
        def __init__(self):
            self.status_code = 500

    mock = MockResponse()

    expected = "\x1b[31m500 SERVER ERROR WITH LINK: https://google.ca\x1b[0m\n"
    lc.status_check_500(mock, "https://google.ca")
    captured = capsys.readouterr()

    assert captured.out == expected
