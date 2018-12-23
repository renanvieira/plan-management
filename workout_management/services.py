import logging
from flask import current_app as app
import sendgrid
from sendgrid.helpers.mail import *

logger = logging.getLogger(__name__)


class SendGrindService(object):

    def __init__(self, api_key):
        self.__api_key = api_key
        self._from = app.config["MAIL_FROM"]
        self.__client = sendgrid.SendGridAPIClient(apikey=api_key)

    def send(self, to, subject, text):
        try:
            if not self.__api_key:
                return

            to_email = Email(to)
            content = Content("text/html", text)

            mail = Mail(Email(self._from), subject, to_email, content)

            response = self.__client.client.mail.send.post(request_body=mail.get())

            logger.info(f"status_code: {response.status_code} - body: {response.body} - headers: {response.headers}")
        except Exception as e:
            logger.exception(e)
            pass
