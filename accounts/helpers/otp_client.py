from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings


def send_otp_email(user_email, user_name, otp, reason=''):
    context = {
        'user_name': user_name,
        'otp': otp,
        'validity_period': 10,
        'company_name': 'AI Challenge',
        'current_year': timezone.now().year,
        'action': 'Verify Email' if not reason else reason
    }
    
    # Render the HTML email template with context
    html_content = render_to_string('accounts/emailtemplate.html', context)
    text_content = strip_tags(html_content)  

    subject = f"Your One-Time Password (OTP) to {'Verify Email' if not reason else reason}"
    from_email = settings.EMAIL_HOST_USER
    to_email = user_email
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    
    # Send the email
    email.send()

def invite_challenge_mail():
    pass
