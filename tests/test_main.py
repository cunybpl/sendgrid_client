import pytest
from sendgrid_api.main import Emails, DummyBackend, SendgridBackend, send_emails
import sendgrid


def test_good_emails():
    Emails(["test1@test.com", "test2@test.com"])


def test_bad_emails():
    with pytest.raises(ValueError):
        Emails(["validemail@test.com", "this is not an email address"])


def test_dummy_backend():
    to_emails = Emails(["test1@test.com", "test2@test.com"])
    result = send_emails(
        to_emails=to_emails,
        from_email="test3@test.com",
        backend=DummyBackend(),
        subject="Testing subject",
        content="Testing content",
    )

    assert result == (
        "Dummy backend!\n"
        + "Recipients: test1@test.com test2@test.com\n"
        + "Sender address: test3@test.com\n"
        + "Subject: Testing subject\n"
        + "Content: Testing content"
    )


def test_sendgrid_backend_401():
    to_emails = Emails(["test1@test.com", "test2@test.com"])
    with pytest.raises(Exception):
        send_emails(
            to_emails=to_emails,
            from_email="test3@test.com",
            backend=SendgridBackend(sendgrid_api_key="invalid api key"),
            subject="Testing subject",
            content="Testing content",
        )


def test_sendgrid_backend(mocker):
    mocked = mocker.patch.object(sendgrid.SendGridAPIClient, "send", return_value=True)

    to_emails = Emails(["test1@test.com", "test2@test.com"])
    result = send_emails(
        to_emails=to_emails,
        from_email="test3@test.com",
        backend=SendgridBackend(sendgrid_api_key="doesn't matter"),
        subject="Testing subject",
        content="Testing content",
    )
    assert result
    assert mocked.called_once()
