from rest_framework import serializers
from .models import CompanyUser, File
class CompanyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUser
        fields = ['id', 'username', 'email', 'user_type', 'email_verified']
class FileSerializer(serializers.ModelSerializer):
    uploaded_by = CompanyUserSerializer(read_only=True)  
    class Meta:
        model = File
        fields = ['id', 'name', 'file', 'file_type', 'created_at', 'uploaded_by']

