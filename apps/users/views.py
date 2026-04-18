from rest_framework import viewsets, mixins
from . import serializers
from . import models

class UserView(viewsets.GenericViewSet,
               mixins.UpdateModelMixin, 
               mixins.RetrieveModelMixin):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer