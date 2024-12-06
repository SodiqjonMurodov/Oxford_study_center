from django.core.mail import send_mail

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