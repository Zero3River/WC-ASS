import re
import pytest

def check_url_validity(url):
    url_regex = (
        r"^(https?:\/\/)"                    # Protocol
        r"((www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.)"  # Domain
        r"[a-zA-Z0-9()]{1,6}\b"              # TLD
        r"([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$"  # Port、path、query、segment
    )
    return bool(re.match(url_regex, url))


@pytest.mark.parametrize("url, expected", [
    ("https://www.example.com", True),
    ("http://example.com", True),
    ("https://sub.domain.com/path?query=123#fragment", True),
    ("https://example.com:8080", True),
    ("http://example.com/index.html", True),
    ("https://example.com/path_with_underscore", True),
    ("ftp://example.com", False),  # wrong protocal
    ("htt://example.com", False),  # typo
    ("https://example", False),    # missing TLD
    ("https:/example.com", False), # missing slash
    ("https:// example.com", False), # space
    ("example.com", False),         # no protocal
])
def test_check_url_validity(url, expected):
    assert check_url_validity(url) == expected

