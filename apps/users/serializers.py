import queue

from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from . import models
from datetime import date
import httpx
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'cpf',
                  'bio',
                  'profile_image',
                  ]
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
    
    def validate_zip_code(self, value):
        zip_code = "".join(filter(str.isdigit, value))

        if len(zip_code) != 8:
            raise serializers.ValidationError("O CEP deve conter exatamente 8 dígitos.")

        return zip_code
    
    def validate(self, attrs):
        zip_code = attrs.get("zip_code")
        
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"https://viacep.com.br/ws/{zip_code}/json/")
            
            if response.status_code != 200:
                raise serializers.ValidationError({"zip_code": "Serviço de busca de CEP indisponível."})

            viacep_data = response.json()
            
            if viacep_data.get('erro'):
                raise serializers.ValidationError({"zip_code": "CEP inexistente."})

        except httpx.RequestError:
            raise serializers.ValidationError({"zip_code": "Erro de conexão ao validar o CEP."})

        # Mapeamento
        mapping = {
            "street": "logradouro",
            "neighborhood": "bairro",
            "city": "localidade",
            "state": "uf",
        }

        for field, viacep_field in mapping.items():
            val = viacep_data.get(viacep_field)
            if val:
                attrs[field] = val

        return attrs
    
class BecomeArtisanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'is_artisan']
        read_only_fields = ['id', 'username']



class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=models.User.objects.all(), message="Este e-mail já está em uso.")]
    )
    first_name = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
    )

    last_name = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
    )
    phone_number = serializers.CharField(required=False, allow_blank=True)
    cpf = serializers.CharField(
        required=False, 
        allow_blank=True, 
        allow_null=True,
        validators=[UniqueValidator(queryset=models.User.objects.all(), message="Este CPF já está em uso.")]
    )
    date_of_birth = serializers.DateField(required=False)

    def validate_cpf(self, value):
        cpf = "".join(filter(str.isdigit, value))

        if len(cpf) != 11:
             raise serializers.ValidationError("O CPF deve conter exatamente 11 dígitos.")
        
        from validate_docbr import CPF
        cpf_validator = CPF()

        if not cpf_validator.validate(cpf):
            raise serializers.ValidationError("CPF inválido.")
        
        return cpf
    
    def validate_date_of_birth(self, value):
        today = date.today()
        
        if value > today:
            raise serializers.ValidationError("A data de nascimento não pode ser no futuro.")

        AGE_OF_MAJORITY = 18
        try:
            limit_date = date(today.year - AGE_OF_MAJORITY, today.month, today.day)
        except ValueError: # Tratamento para anos bissextos
            limit_date = date(today.year - AGE_OF_MAJORITY, today.month, today.day - 1)

        if value > limit_date:
            raise serializers.ValidationError("Você deve ter pelo menos 18 anos.")
        
        return value

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'cpf': self.validated_data.get('cpf', ''),
            'date_of_birth': self.validated_data.get('date_of_birth'),
        })
        return data

    def save(self, request):
        user = super().save(request)

        user.first_name = self.validated_data.get('first_name')
        user.last_name = self.validated_data.get('last_name')
        user.phone_number = self.validated_data.get('phone_number')
        user.cpf = self.validated_data.get('cpf')
        user.date_of_birth = self.validated_data.get('date_of_birth')

        user.save()
        return user
    