import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_message(_from: str, password: str, to: str, subject: str, message: str, file_path: str = "None"):
    msg = MIMEMultipart()
    msg['From'] = _from
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    if (file_path != "None"):
        with open(file_path, 'r') as file:            
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={file_path}')
            msg.attach(part)

    text = msg.as_string()

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(_from, password)
    server.sendmail(_from, to, text)
    server.quit()