from .models import User, Book
from rest_framework import viewsets, permissions
from .serializers import UserSerializer


class UserViewSet (viewsets.ModelViewSet):
  queryset = User.objects.all()
  permission_classes = [permissions.AllowAny]
  serializer_class = UserSerializer
