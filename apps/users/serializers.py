from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 
                  'username',
                  'email',
                  'name',
                  'cpf',
                  ''
                  'bio',
                  ]
        extra_kwargs = {'cpf': {'read_only': True}}
        read_only_fields = ['cpf',]