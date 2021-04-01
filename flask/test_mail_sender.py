import pytest
import smtplib

from .mail_sender import send_email

from email.mime.text import MIMEText
from smtplib import SMTP_SSL


class MockMIMEText:
    def __init__(self, title, ltype):
        self.title = title
        self.type = ltype
        self.dict = {}

    def __setitem__(self, key, item):
        self.dict[key] = item

    def __getitem__(self, key):
        return self.dict[key]

class MockSTMPSSL:
    def __init__(self, host='localhost', port=465):
        self.host = host
        self.port = port
    
    def login(self, user, password):
        self.open_connection = True

    def sendmail(self, src, dest, message):
        pass

    def quit(self):
        self.open_connection = False

def test_send_email(monkeypatch):

    MIMEText = MockMIMEText
    monkeypatch.setattr(smtplib, 'SMTP_SSL', lambda host, port: MockSTMPSSL(host, port))
    send_email('receiver', ['anecdote1'])

    monkeypatch.setattr()
