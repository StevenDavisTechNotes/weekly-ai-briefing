import pytest

from weekly_ai_briefing.config import RECIPIENTS, SENDER_EMAIL
from weekly_ai_briefing.email_briefing import mailer


class FakeImap:
    def __init__(self, lines):
        self.lines = lines

    def list(self):
        return "OK", self.lines


GMAIL_LINES = [
    b'(\\HasNoChildren) "/" "INBOX"',
    b'(\\HasNoChildren \\Sent) "/" "[Gmail]/Sent Mail"',
    b'(\\HasNoChildren \\Trash) "/" [Gmail]/Trash',
    None,
]


def test_find_special_folder_quotes_name():
    imap = FakeImap(GMAIL_LINES)
    assert mailer.find_special_folder(imap, r"\Sent") == '"[Gmail]/Sent Mail"'
    assert mailer.find_special_folder(imap, r"\Trash") == '"[Gmail]/Trash"'


def test_find_special_folder_missing_raises():
    with pytest.raises(RuntimeError):
        mailer.find_special_folder(FakeImap(GMAIL_LINES[:1]), r"\Sent")


def test_build_message_addresses_all_recipients():
    message = mailer.build_message(SENDER_EMAIL, "Subj", "Body")
    assert message["Subject"] == "Subj"
    assert message["To"] == ", ".join(RECIPIENTS)
    assert message["Message-ID"].endswith("@gmail.com>")


def test_sender_is_recipient_ignores_case_and_display_name():
    assert mailer.sender_is_recipient(SENDER_EMAIL.upper())
    assert not mailer.sender_is_recipient("someone@else.com")


def test_send_email_requires_password(monkeypatch):
    monkeypatch.delenv("GMAIL_APP_PASSWORD", raising=False)
    with pytest.raises(RuntimeError, match="GMAIL_APP_PASSWORD"):
        mailer.send_email("s", "b")


class FakeSmtp:
    sent: list = []

    def __init__(self, host, port):
        self.logged_in = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def login(self, user, password):
        self.logged_in = (user, password)

    def send_message(self, message):
        FakeSmtp.sent.append((self.logged_in, message))


@pytest.fixture
def deleted_copies(monkeypatch):
    FakeSmtp.sent = []
    monkeypatch.setattr(mailer.smtplib, "SMTP_SSL", FakeSmtp)
    monkeypatch.setenv("GMAIL_APP_PASSWORD", "secret")
    deleted = []
    monkeypatch.setattr(mailer, "delete_sent_copy", lambda *args: deleted.append(args))
    return deleted


def test_send_email_to_self_keeps_single_copy(deleted_copies, monkeypatch):
    monkeypatch.delenv("GMAIL_USER", raising=False)
    mailer.send_email("Subj", "Body")
    assert len(FakeSmtp.sent) == 1
    assert FakeSmtp.sent[0][0] == (SENDER_EMAIL, "secret")
    assert deleted_copies == []


def test_send_email_from_other_account_deletes_sent_copy(deleted_copies, monkeypatch):
    monkeypatch.setenv("GMAIL_USER", "other@example.com")
    mailer.send_email("Subj", "Body")
    ((sender, password, message_id),) = deleted_copies
    assert (sender, password) == ("other@example.com", "secret")
    assert message_id == FakeSmtp.sent[0][1]["Message-ID"]
