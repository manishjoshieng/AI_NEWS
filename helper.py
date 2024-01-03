from datetime import datetime
from emailClient import *

POST_DATE_FORMAT    =   "%Y-%m-%d %H:%M:%S"
FINAL_DATE_FORMATE  =   "%B %d, %Y"

def print_function_name(func):
    def wrapper(*args, **kwargs):
        # Check if the function is a class method
        if args and hasattr(args[0], '__class__'):
            class_name = args[0].__class__.__name__
            print(f"Calling method: {class_name}.{func.__name__}")
        else:
            print(f"Calling function: {func.__name__}")

        result = func(*args, **kwargs)
        return result
    return wrapper

def dateToStr(date: datetime, formate = POST_DATE_FORMAT) -> str:
    return date.strftime(formate)

def strToDate(date_str: str, formate = POST_DATE_FORMAT) -> datetime:
    return datetime.strptime(date_str, formate)


def sendmail(data:dict):
    mail_clinet = Mail()
    name = data.get("username")
    name = name.title()
    email_id = data.get("email_id")
    phone = data.get("phone_no")
    message = data.get("message")
    subject = f"You receive the feedback from {name}"
    to_email = EMAIL_ID
    content = f'''
    <h2> Name       :   {name} </h2>
    <h2> Email Id   :   {email_id} </h2>
    <h2> Phone      :   {phone}</h2>
    <h2> Message    :</h2>
    <p> {message} </p>
'''
    mail_clinet.sendMail(to_email=[to_email],
                         subject=subject,
                         html_content = content)