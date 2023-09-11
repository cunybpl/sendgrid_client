import abc
from typing import List, Dict, Any
import sendgrid
import sendgrid.helpers.mail as sgm
from sendgrid_api import config
import dotenv


class Email:
    to_email: str
    from_email: str
    subject: str
    content: str

    def __init__(
        self, to_email: str, from_email: str, subject: str, content: str
    ) -> "Email":
        self.to_email = to_email
        self.from_email = from_email
        self.subject = subject
        self.content = content

    def __str__(self) -> str:
        return f"To: {self.to_email}\nFrom: {self.from_email}\nSubject: {self.subject}\nContent: {self.content}"


Emails = List[Email]


class BaseBackend(abc.ABC):
    def send_messages(messages: Emails) -> Any:
        raise NotImplementedError(
            "send_messages must be implemented in child classes of BaseBackend"
        )


class DummyBackend(BaseBackend):
    def send_messages(messages: Emails) -> Any:
        for email in messages:
            print("Dummy backend didn't do anything!")
        return len(messages)


class SendgridBackend(BaseBackend):
    def send_messages(messages: Emails) -> Any:
        api_key = config.SENDGRID_API_KEY
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        for email in messages:
            mail = sgm.Mail(
                from_email=sgm.From(email.from_email),
                to_emails=sgm.To(email.to_email),
                subject=email.subject,
                html_content=sgm.Content("text/html", email.content),
            )
            response = sg.client.mail.send.post(request_body=mail.get())
            return response.status_code


# Our entrypoint
def send_emails(emails: Emails):
    dotenv.load_dotenv()
    backend_class: BaseBackend = (
        SendgridBackend if config.ENVIRONMENT == "production" else DummyBackend
    )
    return backend_class.send_messages(emails)
