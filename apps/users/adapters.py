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
