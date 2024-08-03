import threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from celery import shared_task

class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject = data['subject'],
            body=data['body'],
            to = [data['to_email']]
        )
        if data.get('content_type') == 'html':
            email.content_subtype ='html'
        EmailThread(email).start()


@shared_task()
def send_email(email,code):
    html_content = render_to_string(
        'email/auth/email_avtivate.html',
        {'code':code}
    )
    Email.send_email(
        {
            'subject':'Royhatdan otish uchun',
            'to_email':email,
            "body": html_content,
            'content_type':'html'
        }
    )