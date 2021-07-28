from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import RegistrationEmail, User, CHOICES


class RegEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(read_only=True)

    class Meta:
        model = RegistrationEmail
        fields = ['email', 'confirmation_code']


class RegUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField()

    def validate_email(self, value):
        code = self.initial_data['confirmation_code']
        email = self.initial_data['email']
        email_conf = get_object_or_404(RegistrationEmail, email=email)
        conf_code = email_conf.confirmation_code
        if code != conf_code:
            raise serializers.ValidationError(
                "Неправильный код подтверждения")
        return super().validate(value)

    class Meta:
        fields = ('email', 'username')
        model = User
        validators = []


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(max_length=300, required=False)
    role = serializers.ChoiceField(choices=CHOICES, required=False)
    email = serializers.EmailField()

    class Meta:
        fields = ('first_name', 'last_name',
                  'username', 'bio', 'email', 'role')
        model = User
