from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import ProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from membership.models import Profile


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
