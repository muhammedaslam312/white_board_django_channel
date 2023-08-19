from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
        )

        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True, "required": True},
            "first_name": {"required": True},
        }
