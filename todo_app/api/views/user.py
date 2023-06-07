from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from todo_app.models import User

from ..serializers import UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    Register new users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
