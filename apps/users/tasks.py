from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task(
    name="Envio_de_emails",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send_celery_mail(template_prefix, email, context):

    subject = render_to_string(
        f"{template_prefix}_subject.txt",
        context
    ).strip()

    html_content = render_to_string(
        f"{template_prefix}_message.html",
        context
    )

    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )

    msg.attach_alternative(html_content, "text/html")

    msg.send(fail_silently=False)