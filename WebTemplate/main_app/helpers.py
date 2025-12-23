"""
Helper functions for the main_app module.

This module provides utility functions for email operations, including
fetching and processing emails from an IMAP server.
"""

import imaplib, email, os
from email.header import decode_header
from typing import Any, List, Optional, Tuple, Union
from email.message import Message


def fetch_email_data() -> None:
    """
    Fetch and process email data from an IMAP server.

    This function connects to a configured IMAP mail server, retrieves the most
    recent email(s) from the INBOX, and saves any attachments to the local
    filesystem. It processes both the email headers (subject, sender) and
    multipart message bodies, extracting attachments when present.

    The function performs the following steps:
        1. Establishes an SSL connection to the IMAP server
        2. Authenticates with stored credentials
        3. Selects the INBOX folder
        4. Fetches the most recent email(s)
        5. Decodes email headers (Subject, From)
        6. Iterates through multipart message parts
        7. Saves attachments to the Documents folder

    Returns:
        None

    Raises:
        imaplib.IMAP4.error: If authentication fails or IMAP operations fail.
        OSError: If file operations fail when saving attachments.

    Note:
        - Credentials are hardcoded in this function (security concern).
        - The attachment is saved with a fixed filename, overwriting any
          existing file with that name.
        - Only the most recent email is processed (messages_number=1).

    TODO:
        - Consider moving credentials to environment variables or a config file.
        - The attachment filepath uses a hardcoded filename which may cause
          issues when processing multiple attachments.
        - The bare except clause on line 40 silently swallows all exceptions;
          consider handling specific exceptions or logging errors.
    """
    # IMAP server credentials and connection settings
    username: str = "simpleboard@fintechdocs.ru"
    password: str = "XXXXXXXXXX"
    imap_server: str = "mail.hosting.reg.ru"

    # Establish secure SSL connection to the IMAP server
    imap: imaplib.IMAP4_SSL = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)

    status: str
    messages: Any  # Initially List[bytes], then int
    # Select the INBOX folder and get the total message count
    status, messages = imap.select("INBOX")

    # Number of recent messages to process (starting from most recent)
    messages_number: int = 1
    # Convert the message count from bytes to integer
    messages = int(messages[0])

    # Iterate through messages in reverse order (newest first)
    for i in range(messages, messages-messages_number, -1):
        res: str
        msg_data: List[Union[Tuple[bytes, bytes], bytes]]
        # Fetch the complete email message (RFC822 format)
        res, msg_data = imap.fetch(str(i), "(RFC822)")

        # Process each response part from the fetch operation
        for response in msg_data:
            if isinstance(response, tuple):
                # Parse the raw email bytes into a Message object
                msg: Message = email.message_from_bytes(response[1])

                # Decode the email subject header
                subject: Union[str, bytes]
                encoding: Optional[str]
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)

                # Decode the sender (From) header
                From: Union[str, bytes]
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)

                # Handle multipart messages (emails with attachments or HTML/plain text parts)
                if msg.is_multipart():
                    # Walk through all parts of the multipart message
                    for part in msg.walk():
                        content_type: str = part.get_content_type()
                        content_disposition: str = str(part.get("Content-Disposition"))

                        # Attempt to decode the message body
                        try:
                            body: str = part.get_payload(decode=True).decode()
                        except:
                            # Silently ignore decode errors (e.g., binary attachments)
                            # TODO: Consider logging these errors for debugging
                            pass

                        # Check if this part is an attachment
                        if "attachment" in content_disposition:
                            # Decode the attachment filename
                            filename: Union[str, bytes]
                            filename, encoding = decode_header(part.get_filename())[0]
                            if isinstance(filename, bytes):
                                filename = filename.decode(encoding)

                            # Construct the filepath for saving the attachment
                            # Note: Uses a hardcoded filename rather than the actual attachment name
                            filepath: str = os.path.join(os.getcwd(), "Documents", "XXXXXXXXXX.xlsx")
                            print(filepath)
                            # print(f"folder_name {folder_name}")
                            print(f"email{i}")

                            # Save the attachment to disk
                            open(filepath, "wb").write(part.get_payload(decode=True))

                # Visual separator between processed emails
                print("="*100)

    # Clean up: close the mailbox and logout from the server
    imap.close()
    imap.logout()
