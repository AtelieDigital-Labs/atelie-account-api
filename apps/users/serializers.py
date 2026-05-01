from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from . import models
from datetime import date


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 
                  'username',
                  'email',
                  'name',
                  'cpf',
                  'bio',
                  ]
        extra_kwargs = {'cpf': {'read_only': True}}
        read_only_fields = ['cpf',]
    
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAddress
        fields = [
            'id',
            'user',
            'street',
            'number', 
            'complement',
            'neighborhood',
            'city',
            'state',
            'zip_code',
            'is_main'
        ]
        read_only_fields = ['user',]

class BecomeArtisanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'is_artisan']
        read_only_fields = ['id', 'username']



class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    cpf = serializers.CharField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False)

    # def validate_date_of_birth(self, value):
    #     today = date.today()

    #     age = today.year - value.year - (
    #         (today.month, today.day) < (value.month, value.day)
    #     )

    #     if age < 18:
    #         raise serializers.ValidationError(
    #             "Você precisa ser maior de idade para se cadastrar."
    #         )

    #     return value

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'name': self.validated_data.get('name', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'cpf': self.validated_data.get('cpf', ''),
            'date_of_birth': self.validated_data.get('date_of_birth'),
        })
        return data

    def save(self, request):
        user = super().save(request)

        user.name = self.validated_data.get('name', '')
        user.phone_number = self.validated_data.get('phone_number')
        user.cpf = self.validated_data.get('cpf')
        user.date_of_birth = self.validated_data.get('date_of_birth')

        user.save()
        return user