import httpx
from ..models import Address
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "user",
            "street",
            "number",
            "complement",
            "neighborhood",
            "city",
            "state",
            "zip_code",
            "is_main",
        ]
        read_only_fields = [
            "user",
        ]

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
                raise serializers.ValidationError(
                    {"zip_code": "Serviço de busca de CEP indisponível."}
                )

            viacep_data = response.json()

            if viacep_data.get("erro"):
                raise serializers.ValidationError({"zip_code": "CEP inexistente."})

        except httpx.RequestError:
            raise serializers.ValidationError(
                {"zip_code": "Erro de conexão ao validar o CEP."}
            )

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
