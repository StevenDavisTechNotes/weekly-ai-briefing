# Environment:
#   GMAIL_USER          optional; sending account (default: the recipient address)
#   GMAIL_APP_PASSWORD  required;
#        a Google app password for the sending account
#        see https://myaccount.google.com/apppasswords

import imaplib
import os
import smtplib
import time
from email.message import EmailMessage
from email.utils import make_msgid, parseaddr

from weekly_ai_briefing.config import (
    IMAP_HOST,
    RECIPIENTS,
    SENDER_EMAIL,
    SENT_COPY_ATTEMPTS,
    SENT_COPY_DELAY_SECONDS,
    SMTP_HOST,
    SMTP_PORT,
)


def find_special_folder(imap: imaplib.IMAP4_SSL, attribute: str) -> str:
    r"""Returns the quoted name of the mailbox flagged with attribute, e.g. \Sent.

    Gmail's folder names are localized ("[Gmail]/Sent Mail", "[Google Mail]/...")
    but the special-use attributes are not.
    """
    _, lines = imap.list()
    for line in lines:
        if not isinstance(line, bytes):
            continue
        flags = line.split(b")", 1)[0].split()
        if attribute.encode() in flags:
            name = line.decode().rsplit(' "/" ', 1)[1]
            return name if name.startswith('"') else f'"{name}"'
    raise RuntimeError(f"No {attribute} mailbox found")


def delete_sent_copy(sender: str, password: str, message_id: str) -> None:
    """Permanently deletes the copy Gmail saved in the sender's Sent folder."""
    with imaplib.IMAP4_SSL(IMAP_HOST) as imap:
        imap.login(sender, password)
        sent_folder = find_special_folder(imap, r"\Sent")
        trash_folder = find_special_folder(imap, r"\Trash")

        imap.select(sent_folder)
        for _ in range(SENT_COPY_ATTEMPTS):
            _, data = imap.uid("SEARCH", "HEADER", "Message-ID", message_id)
            uids = data[0]
            if isinstance(uids, bytes) and uids:
                break
            time.sleep(SENT_COPY_DELAY_SECONDS)
            imap.noop()
        else:
            print(f"  Sent copy of {message_id} not found; leaving it")
            return
        # In Gmail, expunging from Sent only removes the label; the message must
        # go through Trash to actually be deleted.
        imap.uid("MOVE", uids.decode().replace(" ", ","), trash_folder)

        imap.select(trash_folder)
        _, data = imap.uid("SEARCH", "HEADER", "Message-ID", message_id)
        uids = data[0]
        if isinstance(uids, bytes) and uids:
            imap.uid("STORE", uids.decode().replace(" ", ","), "+FLAGS", r"(\Deleted)")
            imap.expunge()
    print("  Deleted the sent copy")


def build_message(sender: str, subject: str, body: str) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(RECIPIENTS)
    message["Message-ID"] = make_msgid(domain=sender.split("@")[-1])
    message.set_content(body)
    return message


def sender_is_recipient(sender: str) -> bool:
    return parseaddr(sender)[1].lower() in [parseaddr(x)[1].lower() for x in RECIPIENTS]


def send_email(subject: str, body: str) -> None:
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not password:
        raise RuntimeError("Set GMAIL_APP_PASSWORD to a Google app password")
    sender = os.environ.get("GMAIL_USER", SENDER_EMAIL)
    message = build_message(sender, subject, body)

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(sender, password)
        smtp.send_message(message)
    print(f"Emailed {subject} to {', '.join(RECIPIENTS)}")

    # Mailing yourself stores one message labelled both Inbox and Sent, so
    # there is no second copy to delete (deleting it would empty the Inbox too).
    if not sender_is_recipient(sender):
        delete_sent_copy(sender, password, message["Message-ID"])
