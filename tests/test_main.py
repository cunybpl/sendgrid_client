import pytest
from sendgrid_api import main


def test_main():
    assert main.main() == 1
