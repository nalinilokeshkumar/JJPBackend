from rest_framework import serializers
from .models import User
import bcrypt

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data['password'].encode()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        validated_data['password'] = hashed.decode()
        return User.objects.create(**validated_data)