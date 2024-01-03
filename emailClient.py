from smtplib import SMTP
from email.message import EmailMessage
import os

EMAIL_ID = os.environ.get("SENDER_EMAIL_ID")
EMAIL_KEY = os.environ.get("SENDER_EMAIL_KEY")


class Mail:
    def __init__(self) -> None:
        self.email_id = EMAIL_ID
        self.password = EMAIL_KEY
        self.valid_hosts = {"gmail" : "smtp.gmail.com","hotmail" : "smtp.live.com","yahoo": "smtp.mail.yahoo.com"}
        self.host = self._parseHost(self.email_id)
        
    
    def _parseHost(self,email_id):
        check1="@"
        check2=".com"
        host = None
        if check1 in email_id and check2 in email_id:
            index1 = email_id.index(check1)+1
            index2 = email_id.index(check2)
            if index1 < index2:
                host = email_id[index1:index2]
                if host in self.valid_hosts:
                    host = self.valid_hosts[host]
                    return host
        if host == None:
            print(f"Warning: {email_id} is not valid email address!")
        return host
        
    def sendMail(self,to_email: list,subject:str, body : str = None, html_content:str = None):
        try:
            client = SMTP(self.host)
            client.starttls()
        except:
            print(f"Error: {self.email_id} is not from supported host")
            return

        try:
            #login
            client.login(user=self.email_id,password=self.password)
        except:
            print("Error: Authentication fail. Check your password")
            return
        else:
            print("Login successful")
            if type(to_email) is not list:
                receiveres = [to_email]
            else:
                receiveres = to_email

            try:
                for receiver in receiveres:
                    #send mail
                    msg = EmailMessage()
                    if html_content is not None:
                         msg.add_alternative(html_content, subtype="html")
                    elif body is not None:
                        msg.set_content(body)

                    msg['Subject'] = subject
                    msg['From'] = self.email_id
                    msg['To'] = receiver

                    client.send_message(msg)
                    print(f"Email sent Successfully to {receiver}")
            except Exception as e:
                print(f"Error: Email send fail: {e}")
            finally:
                client.close()
