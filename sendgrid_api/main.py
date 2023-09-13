import abc
from typing import List, Any
import sendgrid  # type: ignore
import sendgrid.helpers.mail as sgm  # type: ignore
import re


class Emails:
    addresses: List[str]
    _email_regex: str = r"^\S+@\S+\.\S+$"

    def __init__(self, addresses: List[str]) -> None:
        self.addresses = [self._validate(a) for a in addresses]

    def _validate(self, email: str) -> str:
        if not re.fullmatch(self._email_regex, email):
            raise ValueError(f"Email address {email} is invalid")
        return email

    def __str__(self) -> str:
        return " ".join(self.addresses)


class EmailMessenger(abc.ABC):
    @abc.abstractmethod
    def send_messages(
        self,
        addresses_to: Emails,
        address_from: str,
        subject: str,
        content: str,
    ) -> Any:
        pass


class DummyBackend(EmailMessenger):
    def __init__(self) -> None:
        super().__init__()

    def send_messages(
        self,
        addresses_to: Emails,
        address_from: str,
        subject: str,
        content: str,
    ) -> Any:
        return (
            f"Dummy backend!\nRecipients: {addresses_to}\n"
            + f"Sender address: {address_from}\n"
            + f"Subject: {subject}\n"
            + f"Content: {content}"
        )


class SendgridBackend(EmailMessenger):
    def __init__(self, sendgrid_api_key: str) -> None:
        super().__init__()
        self.client = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)

    def send_messages(
        self,
        addresses_to: Emails,
        address_from: str,
        subject: str,
        content: str,
    ) -> Any:
        mail = sgm.Mail(
            from_email=sgm.From(address_from),
            to_emails=[sgm.To(address) for address in addresses_to.addresses],
            subject=subject,
            html_content=sgm.Content(mime_type="text/html", content=content),
        )
        return self.client.send(mail)


# Entrypoint
def send_emails(
    to_emails: Emails,
    from_email: str,
    backend: EmailMessenger,
    subject: str,
    content: str,
) -> Any:
    return backend.send_messages(
        addresses_to=to_emails,
        address_from=from_email,
        subject=subject,
        content=content,
    )
