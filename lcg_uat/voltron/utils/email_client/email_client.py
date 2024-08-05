import base64
import binascii
import email
import imaplib
import logging
from typing import NamedTuple

from voltron.utils.exceptions.general_exception import GeneralException
from voltron.utils.helpers import cleanhtml


class EmailClient(object):
    def __init__(self,
                 username: str,
                 password: str,
                 imap_host: str = 'imap.gmail.com',
                 imap_port: int = 993,
                 brand: str = 'bma',
                 **kwargs):

        self.brand = brand
        imap_conn = imaplib.IMAP4_SSL(imap_host, imap_port)

        imap_conn.login(username, password)
        imap_conn.select('Inbox')
        self.imap_conn = imap_conn
        self._logger = logging.getLogger('voltron_logger')

    def _get_emails(self):
        """
        Internal method to get all emails in selected folder

        :return: List of Basic message objects (email.message.Message)
        """
        i = self.imap_conn
        result, data = i.uid('search', None, "ALL")
        if result != 'OK':
            raise GeneralException(f'Something wrong with connection to Gmail: "{result}"')

        emails = []

        for num in data[0].split():
            result_, data_ = i.uid('fetch', num, '(RFC822)')
            if result_ != 'OK':
                raise GeneralException(f'Something wrong with connection to Gmail: "{result}"')
            email_message = email.message_from_bytes(data_[0][1])
            emails.append(email_message)

        self._logger.debug(f'*** Found {len(emails)} emails in current folder')
        return emails

    def _get_email_body(self, mail):
        """
        Internal method to get email body as a text
        :param mail:
        :return:
        """
        maintype = mail.get_content_maintype()
        self._logger.debug(f'*** Email maintype is "{maintype}"')
        if maintype == 'multipart':
            for part in mail.get_payload():
                if part.get_content_maintype() == 'text':
                    try:
                        body = ' '.join(cleanhtml(base64.b64decode(part.get_payload()).decode('utf-8')).split())
                    except (binascii.Error, UnicodeDecodeError):
                        body = ' '.join((part.get_payload()).split())
                    self._logger.debug(f'*** Body: {body}')
        elif maintype == 'text':
            body = ' '.join(cleanhtml(base64.b64decode(mail.get_payload()).decode('utf-8')).split())
        else:
            self._logger.warning(f'*** Unsupported maintype {maintype}')
            body = ''
        self._logger.debug(f'*** Body: {body}')
        return body

    def read_emails(self, **kwargs):
        """
        Reads all emails in Inbox
        Returns list of named tuples with event data: From, Subject, Body
        By default - returns all emails
        :return:
        """
        all_emails = self._get_emails()

        emails = []
        _email = NamedTuple('email', [('sender', str), ('subject', str), ('body', str)])

        expected_subject = kwargs.get('subject', None)

        for one_email in all_emails:
            sender = one_email['From']
            self._logger.debug(f'*** From: {sender}')
            subject = one_email['Subject']
            self._logger.debug(f'*** Subject: {subject}')
            if expected_subject and expected_subject != subject:
                continue

            body = self._get_email_body(mail=one_email)
            emails.append(_email(sender, subject, body))

        self._logger.info(f'*** Found {len(emails)} emails')
        self._logger.debug(f'*** Found emails: {emails}')
        return emails

    def delete_emails(self, subject: str):
        """
        Method used to delete emails by subject
        :param subject: Subject
        :return:
        """
        i = self.imap_conn
        result, data = i.uid('search', None, "ALL")
        if result != 'OK':
            raise GeneralException(f'Something wrong with connection to Gmail: "{result}"')
        for num in data[0].split():
            result_, data_ = i.uid('fetch', num, '(RFC822)')
            if result_ != 'OK':
                raise GeneralException(f'Something wrong with connection to Gmail: "{result}"')
            email_message = email.message_from_bytes(data_[0][1])
            sender = email_message['From']
            self._logger.debug(f'*** From: {sender}')
            actual_subject = email_message['Subject']
            self._logger.debug(f'*** Subject: {subject}')

            if subject == actual_subject:
                i.uid('STORE', num, '+FLAGS', '(\\Deleted)')
        i.expunge()
