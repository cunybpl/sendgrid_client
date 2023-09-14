import pytest
import os


@pytest.fixture(scope="module")
def live_test_creds():
    return {
        "api_key": os.environ("SENDGRID_TESTING_API_KEY"),
        "to_emails": ["kgasiorowski123@gmail.com"],
        "from_email": "admin@cunybplservices.net",
    }
