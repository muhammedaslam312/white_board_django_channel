from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .serializers import AccountSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login

User = get_user_model()


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    class UserModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("username", "email", "password", "first_name")

    def post(self, *args, **kwargs):
        serializer = AccountSerializer(data=self.request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_obj = User.objects.create(
            email=serializer.validated_data["email"],
            username=serializer.validated_data["username"],
            first_name=serializer.validated_data["first_name"],
            is_active=True,
        )
        password = serializer.validated_data["password"]
        user_obj.set_password(password)
        user_obj.save()

        return Response(
            self.UserModelSerializer(user_obj).data, status=status.HTTP_201_CREATED
        )


class UserLoginView(APIView):
    serializer_class = AuthTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = self.serializer_class(
            context={"request": request}, data=request.data
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        # Here you are logging in the user
        login(request, user)
        token_obj, created = Token.objects.get_or_create(user=user)

        # Returning the token
        return Response(
            {
                "token": token_obj.key,
            },
            status=status.HTTP_200_OK,
        )
