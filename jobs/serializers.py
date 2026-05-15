from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Job
        fields = '__all__'