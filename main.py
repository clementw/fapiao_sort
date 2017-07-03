import getpass
import imaplib
import email
import os
from email.header import decode_header, make_header


acct = input('email: ')
pwd = getpass.getpass()
server = "imap.qq.com"


def read_email():
    mail = imaplib.IMAP4_SSL(server)
    mail.login(acct, pwd)
    mail.select('inbox')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    for i in range(latest_email_id, latest_email_id - 20, -1):
        i = str(i).encode()
        typ, data = mail.fetch(i, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode("utf-8"))
                email_subject = make_header(decode_header(msg['subject'])).__str__()
                email_from = make_header(decode_header(msg['from'])).__str__()
                print('From : ' + email_from + '\n')
                print('Subject : ' + email_subject + '\n')

            if msg.get_content_maintype() != 'multipart':
                continue

            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                if filename is not None:
                    sv_path = os.path.join(os.getcwd(), filename)
                    if not os.path.isfile(sv_path):
                        print(sv_path)
                        fp = open(sv_path, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()

if __name__ == "__main__":
    read_email()
