from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from .tasks import send_celery_mail

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        # Username (importantíssimo no teu caso)
        if not user.username:
            user.username = user.email.split("@")[0]

        # Foto de perfil
        picture = data.get("picture")
        if picture:
            user.profile_image_url = picture 

        return user

class CeleryAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):

        safe_context = {}

        for key, value in context.items():

            if key == "user":
                safe_context["user_name"] = value.first_name

            elif isinstance(value, (str, int, float, bool, list, dict)):
                safe_context[key] = value

            else:
                safe_context[key] = str(value)

        send_celery_mail.delay(
            template_prefix,
            email,
            safe_context
        )
    