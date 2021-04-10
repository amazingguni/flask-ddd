
from urllib.parse import urlparse


def assert_redirect_response(response, expected_url):
    assert response.status_code == 302
    assert urlparse(response.location).path == expected_url
