import abc
from typing import List, Dict, Any
import sendgrid
import sendgrid.helpers.mail as sgm
from sendgrid_api import config
import jinja2


class BaseBackend(abc.ABC):
    @abc.abstractmethod
    def send_messages(
        addresses_to: List[str],
        address_from: str,
        subject: str,
        content: str | Dict,
    ) -> Any:
        pass


class DummyBackend(BaseBackend):
    def send_messages(
        addresses_to: List[str],
        address_from: str,
        subject: str,
        content: str | Dict,
    ) -> Any:
        print("Dummy backend didn't do anything!")
        return len(addresses_to)


class SendgridBackend(BaseBackend):
    def send_messages(
        addresses_to: List[str],
        address_from: str,
        subject: str,
        content: str | Dict,
    ) -> Any:
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("./sendgrid_api/templates"),
            autoescape="html",
        )

        html = env.get_template("email_template.html").render(**content)

        sg = sendgrid.SendGridAPIClient(api_key=config.SENDGRID_API_KEY)
        mail = sgm.Mail(
            from_email=sgm.From(address_from),
            to_emails=[sgm.To(address) for address in addresses_to],
            subject=subject,
            html_content=sgm.Content("text/html", html),
        )
        response = sg.client.mail.send.post(request_body=mail.get())
        return response.status_code


# Our entrypoint
def send_emails(
    addresses_to: List[str],
    address_from: str,
    subject: str,
    content: str | Dict,
    backend: BaseBackend = SendgridBackend,
):
    return backend.send_messages(
        address_from=address_from,
        addresses_to=addresses_to,
        subject=subject,
        content=content,
    )
