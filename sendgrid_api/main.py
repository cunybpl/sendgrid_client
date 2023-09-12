import abc
from typing import List, Dict, Any, Optional
import sendgrid
import sendgrid.helpers.mail as sgm
from sendgrid_api import config


class BaseBackend(abc.ABC):
    @abc.abstractmethod
    def send_messages(
        self,
        addresses_to: List[str],
        address_from: str,
        subject: str,
        content: str,
    ) -> Any:
        ...


class DummyBackend(BaseBackend):
    def send_messages(
        self,
        addresses_to: List[str],
        address_from: str,
        subject: str,
        content: str,
    ) -> Any:
        print("Dummy backend didn't do anything!")
        return len(addresses_to)


class SendgridBackend(BaseBackend):
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
            plain_text_content=sgm.Content(mime_type="text/plain", content=content),
        )

        sg = sendgrid.SendGridAPIClient(api_key=config.SENDGRID_API_KEY)
        response = sg.client.mail.send.post(request_body=mail.get())
        return response.status_code


_backends: Dict[str, type[BaseBackend]] = {
    "sendgrid": SendgridBackend,
    "dummy": DummyBackend,
}


# Our entrypoint
def send_emails(
    addresses_to: List[str],
    address_from: str,
    subject: str,
    content: str | Dict[str, str],
    backend_str: str,
) -> Any:
    backend = _backends[backend_str]()
    return backend.send_messages(
        address_from=address_from,
        addresses_to=addresses_to,
        subject=subject,
        content=content,
    )
