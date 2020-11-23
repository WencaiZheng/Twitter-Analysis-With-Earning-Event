
import smtplib
from glob import glob
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

today = str(date.today())
msg = MIMEMultipart()

class SendEmail:

    
    def __init__(self,toaddr):

        self.fromaddr = "noven.zheng@gmail.com"
        self.pswd = pd.read_csv('TOKENS\\ETOKEN.txt').columns[0]
        # send to which email address
        self.toaddr = toaddr

    def send_preopen_email(self):
        
        fileaddr= f'data\\preopen\\{today}\\*'

        msg['From'] = self.fromaddr
        msg['To'] = ", ".join(self.toaddr)
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
        server.login(self.fromaddr, self.pswd)
        text = msg.as_string()
        server.sendmail(self.fromaddr, self.toaddr, text)
        server.quit()
        print(f'Email successfully sent to {self.toaddr}')

    def send_regular_email(self):
        
        fileaddr= f'data\\senti_graph\\{today}\\*'
        msg['From'] = self.fromaddr
        msg['To'] = ", ".join(self.toaddr)
        msg['Subject'] = "Twitter sentiment analysis results"
        msg['Cc'] = 'wencai.zheng@hotmail.com'
        body = "Hi Professor, \n This is twitter analysis result for today. \n\n  - Sent by Python"
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
        server.login(self.fromaddr,self.pswd)
        text = msg.as_string()
        server.sendmail(self.fromaddr, self.toaddr, text)
        server.quit()
        print(f'Email successfully sent to {self.toaddr}')


    def send_realtime_email(self,body_):
        """
        msg['From'] = self.fromaddr
        msg['To'] = ", ".join(self.toaddr)
        msg['Subject'] = "[Test] Twitter real time (half) hourly trending alert"
        body = body_
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.fromaddr,self.pswd)
        text = msg.as_string()
        server.sendmail(self.fromaddr, self.toaddr, text)
        server.quit()
        print(f'Email successfully sent to {self.toaddr}')
        """
        import smtplib, ssl

        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = self.fromaddr  # Enter your address
        receiver_email = self.toaddr  # Enter receiver address
        password = self.pswd
        message = f"""\
Subject: [Test] Twitter real time (half) hourly trending alert

{body_}"""

        context = ssl.create_default_context()
        # send to multiple emails
        for receiver in receiver_email:
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver, message)
                
            print(f'Email successfully sent to {receiver}')
    
    def send_election_email(self,body_):
        import smtplib, ssl

        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = self.fromaddr  # Enter your address
        receiver_email = self.toaddr  # Enter receiver address
        password = self.pswd
        message = f"""\
Subject: Election half-hour updates

{body_}"""

        context = ssl.create_default_context()
        # send to multiple emails
        for receiver in receiver_email:
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver, message)
                
            print(f'Email successfully sent to {receiver}')