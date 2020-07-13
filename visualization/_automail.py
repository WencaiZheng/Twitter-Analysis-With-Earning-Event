
import smtplib
from glob import glob
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

today = str(date.today()) 

def send_preopen_email(toaddr):
    
    fileaddr= f'data\\preopen\\{today}\\*'
    fromaddr = "noven.zheng@gmail.com"

    pswd = pd.read_csv('TOKENS\\ETOKEN.txt').columns[0]
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)
    msg['Subject'] = "Twitter sentiment pre-open analysis results"
    msg['Cc'] = 'wencai.zheng@hotmail.com'
    body = "Hi Professor, \n This is pre-open analysis result for today. \n\n  - Sent by Python"
    msg.attach(MIMEText(body, 'plain'))

    names = glob(fileaddr)
    for filename in names:
        attachment = open(f"{filename}", "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename.split('$')[-1]}" )

        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, pswd)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print(f'Email successfully sent to {toaddr}')