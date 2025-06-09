import imaplib, email, os
from email.header import decode_header


def fetch_email_data():
    username = "simpleboard@fintechdocs.ru"
    password = "XXXXXXXXXX"
    imap_server = "mail.hosting.reg.ru"
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)
    status, messages = imap.select("INBOX")
    messages_number = 1
    messages = int(messages[0])
    for i in range(messages, messages-messages_number, -1):
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if "attachment" in content_disposition:
                            filename, encoding = decode_header(part.get_filename())[0]
                            if isinstance(filename, bytes):
                                filename = filename.decode(encoding)
                            filepath = os.path.join(os.getcwd(), "Documents", "XXXXXXXXXX.xlsx")
                            print(filepath)
                            # print(f"folder_name {folder_name}")
                            print(f"email{i}")
                            open(filepath, "wb").write(part.get_payload(decode=True))
                print("="*100)
    imap.close()
    imap.logout()