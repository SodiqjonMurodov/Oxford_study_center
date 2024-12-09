import re
from django.core.mail import send_mail
from rest_framework.serializers import ValidationError
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")

def check_email(email):
    if not re.fullmatch(email_regex, email):
        data = {
            "success": False,
            "message": "Invalid email"
        }
        raise ValidationError(data)
    else:
        return email


def send_confirmation_email(email, code):
    send_mail(
        subject = 'Код подтверждение',
        message=f'Ваш код подтверждения в Oxford: {code}',
        html_message=f"""
            <h4>Ваш код подтверждения в Oxford:</h4>
            <h1>{code}</h1>
            <p>Проверить приведенный выше код можно исполюзовать перейдя по <a href="http://example.com/confirmation/12346">ссылке</a>.</p>
            """,
        from_email='murodovsodiq1800@gmail.com',
        recipient_list=[email],
        fail_silently=False,
    )

