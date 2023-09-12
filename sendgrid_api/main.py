import abc
from typing import List, Dict, Any, Optional
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
        template_name: str,
    ) -> Any:
        pass


class DummyBackend(BaseBackend):
    def send_messages(
        addresses_to: List[str],
        address_from: str,
        subject: str,
        content: str | Dict,
        template_name: str,
    ) -> Any:
        print("Dummy backend didn't do anything!")
        return len(addresses_to)


class SendgridBackend(BaseBackend):
    def send_messages(
        addresses_to: List[str],
        address_from: str,
        subject: str,
        content: str | Dict,
        template_name: Optional[str] = None,
    ) -> Any:
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("./templates"),
            autoescape="html",
        )

        if isinstance(content, str):
            mail = sgm.Mail(
                from_email=sgm.From(address_from),
                to_emails=[sgm.To(address) for address in addresses_to],
                subject=subject,
                content=sgm.Content("text/plain", content),
            )
        else:
            html = env.get_template(template_name).render(**content)
            mail = sgm.Mail(
                from_email=sgm.From(address_from),
                to_emails=[sgm.To(address) for address in addresses_to],
                subject=subject,
                html_content=sgm.Content("text/html", html),
            )

        sg = sendgrid.SendGridAPIClient(api_key=config.SENDGRID_API_KEY)
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
