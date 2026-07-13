from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from infra.messaging.publishers.user_created import publish_user_created
from infra.messaging.events.user_created import UserCreatedEvent
from asgiref.sync import async_to_sync


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


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=commit)
        
        cleaned_data = getattr(form, "cleaned_data", {})
        user.first_name = cleaned_data.get("first_name", user.first_name)
        user.last_name = cleaned_data.get("last_name", user.last_name)
        user.phone_number = cleaned_data.get("phone_number", user.phone_number)
        user.cpf = cleaned_data.get("cpf", user.cpf)
        user.date_of_birth = cleaned_data.get("date_of_birth", user.date_of_birth)
        
        if commit:
            user.save()
        return user
        
    def send_mail(self, template_prefix, email, context):
        print("SEND_MAIL CHAMADO")
        user = context.get("user")

        event = UserCreatedEvent(
            user_id=user.id,
            first_name=user.first_name,
            email=email,
            confirmation_key=context.get("key"),
            confirmation_url=context.get("activate_url"),
            template_prefix=template_prefix,
        )

        async_to_sync(publish_user_created)(event)

    # async def _publish(self, event):
    #     async with broker:
    #         await broker.publish(
    #             message=asdict(event),
    #             exchange=exchange_accounts,
    #             routing_key=RoutingKey.USER_CREATED_ROUTING_KEY
    #         )
