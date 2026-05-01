from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        # Nome
        user.name = data.get("name", "")

        # Username (importantíssimo no teu caso)
        if not user.username:
            user.username = user.email.split("@")[0]

        # Foto de perfil
        picture = data.get("picture")
        if picture:
            user.profile_image = picture  # depois explico isso melhor 👇

        return user