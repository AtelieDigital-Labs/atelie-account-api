from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from ..serializers.profiles import ProfileSerializer
from drf_spectacular.utils import extend_schema
from ...services import get_user_service
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

@extend_schema(
    tags=["Profile"],
    request=ProfileSerializer,
    responses=ProfileSerializer,
)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    service = get_user_service()

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.service.update(self.request.user, serializer.validated_data)
        return Response(ProfileSerializer(user).data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = self.service.update(self.request.user, serializer.validated_data)
        return Response(ProfileSerializer(user).data, status=status.HTTP_200_OK)
