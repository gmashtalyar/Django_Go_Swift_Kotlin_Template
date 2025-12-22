import imaplib, email, os
from email.header import decode_header
from typing import Any, List, Optional, Tuple, Union
from email.message import Message


def fetch_email_data() -> None:
    username: str = "simpleboard@fintechdocs.ru"
    password: str = "XXXXXXXXXX"
    imap_server: str = "mail.hosting.reg.ru"
    imap: imaplib.IMAP4_SSL = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)
    status: str
    messages: Any  # Initially List[bytes], then int
    status, messages = imap.select("INBOX")
    messages_number: int = 1
    messages = int(messages[0])
    for i in range(messages, messages-messages_number, -1):
        res: str
        msg_data: List[Union[Tuple[bytes, bytes], bytes]]
        res, msg_data = imap.fetch(str(i), "(RFC822)")
        for response in msg_data:
            if isinstance(response, tuple):
                msg: Message = email.message_from_bytes(response[1])
                subject: Union[str, bytes]
                encoding: Optional[str]
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)
                From: Union[str, bytes]
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type: str = part.get_content_type()
                        content_disposition: str = str(part.get("Content-Disposition"))
                        try:
                            body: str = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if "attachment" in content_disposition:
                            filename: Union[str, bytes]
                            filename, encoding = decode_header(part.get_filename())[0]
                            if isinstance(filename, bytes):
                                filename = filename.decode(encoding)
                            filepath: str = os.path.join(os.getcwd(), "Documents", "XXXXXXXXXX.xlsx")
                            print(filepath)
                            # print(f"folder_name {folder_name}")
                            print(f"email{i}")
                            open(filepath, "wb").write(part.get_payload(decode=True))
                print("="*100)
    imap.close()
    imap.logout()