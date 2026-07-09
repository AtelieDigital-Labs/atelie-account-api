

from .context import reset_current_actor, set_current_actor


class AuditContextMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = None

        if hasattr(request, "user") and request.user.is_authenticated:
            token = set_current_actor(str(request.user.pk))

        response = self.get_response(request)

        # Restaura o ContextVar para evitar vazamento entre requisições
        if token is not None:
            reset_current_actor(token)

        return response
