import abc
from typing import List, Dict, Any, Optional
import sendgrid
import sendgrid.helpers.mail as sgm
from sendgrid_api import config


class EmailMessenger(abc.ABC):
    @abc.abstractmethod
    def send_messages(
        self,
        addresses_to: List[str],
        address_from: str,
        subject: str,
        content: str,
    ) -> Any:
        ...


class DummyBackend(EmailMessenger):
    def __init__(self) -> None:
        super().__init__()

    def send_messages(
        self,
        addresses_to: List[str],
        address_from: str,
        subject: str,
        content: str,
    ) -> Any:
        print("Dummy backend didn't do anything!")
        return len(addresses_to)


class SendgridBackend(EmailMessenger):
    def __init__(self, sendgrid_api_key: str) -> None:
        super().__init__()
        self.client = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)

    def send_messages(
        self,
        addresses_to: List[str],
        address_from: str,
        subject: str,
        content: str,
    ) -> Any:
        mail = sgm.Mail(
            from_email=sgm.From(address_from),
            to_emails=[sgm.To(address) for address in addresses_to],
            subject=subject,
            html_content=sgm.Content(mime_type="text/html", content=content),
        )
        response = self.client.client.mail.send.post(request_body=mail.get())
        return response.status_code
