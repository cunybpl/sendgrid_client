import pytest
from sendgrid_api import main


def test_dummy_backend():
    email = main.Email(
        to_email="test@example.com",
        from_email="test@example.com",
        subject="Testing Subject",
        content="<html><h1>Testing content</h2><html>",
    )

    assert main.send_emails([email], main.DummyBackend) == 1
