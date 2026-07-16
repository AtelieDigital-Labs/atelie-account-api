from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from infra.messaging.publishers.user_created import publish_user_created
from infra.messaging.events.user_created import UserCreatedEvent
from asgiref.sync import async_to_sync

import logging

logger = logging.getLogger(__name__)


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
        print("SEND_MAIL CHAMADO", flush=True)
        
        # 1. Print de segurança para ver o que tem dentro do context
        print(f"DEBUG CONTEXTO COMPLETO: {context}", flush=True)
        
        if not context:
            print("ERRO: O dicionário 'context' veio vazio ou nulo!", flush=True)
            return
    
        user = context.get("user")
        key = context.get("key")
        
        print(f"DEBUG - User extraído: {user}", flush=True)
        print(f"DEBUG - Key extraída: {key}", flush=True)
    
        if not user:
            print("ERRO: Não foi possível obter o 'user' do contexto. O fluxo não pode continuar.", flush=True)
            return
    
        if not key:
            print("AVISO: A 'key' veio vazia no contexto.", flush=True)
    
        # 2. Monta a URL com segurança usando f-string pura
        confirmation_url = f"{settings.BACKEND_URL}/auth/confirm-email?key={key or ''}"
        print(f"DEBUG - URL gerada: {confirmation_url}", flush=True)
    
        try:
            event = UserCreatedEvent(
                user_id=user.id,
                first_name=user.first_name,
                email=email,
                confirmation_key=key or "",
                confirmation_url=confirmation_url,
                template_prefix=template_prefix,
            )
            
            print("Tentando publicar evento...", flush=True)
            async_to_sync(publish_user_created)(event)
            print("Evento publicado com sucesso!", flush=True)
            
        except Exception as e:
            print(f"ERRO FATAL DURANTE DISPARO DO EVENTO: {str(e)}", flush=True)
