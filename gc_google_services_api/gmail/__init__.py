from __future__ import print_function

import base64
import json
import os

from email.message import EmailMessage
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# TODO: Remove default value (Just development prupose)
AUTHENTICATION_EMAIL = os.getenv('AUTHENTICATION_EMAIL')
CREDENTIALS_BASE64 = os.getenv('GOOGLE_SHEET_CREDENTIALS', '')
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
]

try:
    CREDENTIALS_CONTENT = json.loads(base64.b64decode(CREDENTIALS_BASE64))
except json.JSONDecodeError as e:
    print('[ERROR CREDENTIALS_CONTENT]: ', e)
    CREDENTIALS_CONTENT = ''


def send_email():
    credentials = service_account.Credentials.from_service_account_info(
        CREDENTIALS_CONTENT,
        scopes=SCOPES)

    creds = credentials.with_subject(AUTHENTICATION_EMAIL)

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content('This is automated draft mail')

        message['to'] = AUTHENTICATION_EMAIL
        message['from'] = AUTHENTICATION_EMAIL
        message['subject'] = 'Automated draft'

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId='me', body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred2: {error}')
        send_message = None

    return send_message
