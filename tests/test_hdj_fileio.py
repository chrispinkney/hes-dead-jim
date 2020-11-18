import pytest
import src.hdj_fileio as fio


# Test that file_check_ignored throws an error if tested with bad filepaths
def test_file_check_ignored_empty_files():
    with pytest.raises(FileNotFoundError):
        fio.file_check_ignored("", "")


# Tests that file_check() still accepts a file and returns a soup object.
def test_file_check():
    tested_output = '<!DOCTYPE html>\n\n<html>\n<head>\n<title>Header</title>\n<meta charset="utf-8"/>\n</head>\n<body>\n<a href="https://github.com/chrispinkney"> Working link here </a>\n<a href="https://senecacollege.ca"> However, this line (and link) should be ignored. </a>\n</body>\n</html>\n'
    soup = fio.file_check("tests/test1.html")
    assert str(soup) == tested_output
