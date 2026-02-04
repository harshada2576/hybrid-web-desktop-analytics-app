"""
Serializers for IIT Bombay Analytics Backend.

Handles data validation and serialization for all API endpoints.
"""

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import DatasetUpload


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Validates email uniqueness and password strength.
    """
    
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'username': {'required': True},
        }
    
    def validate(self, attrs):
        """
        Validate that passwords match.
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs
    
    def create(self, validated_data):
        """
        Create user with hashed password.
        """
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    
    Accepts username and password for authentication.
    """
    
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )


class DatasetUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for dataset upload.
    
    Handles CSV file upload and basic metadata.
    Does not include summary_json as it's computed server-side.
    """
    
    class Meta:
        model = DatasetUpload
        fields = ['id', 'file', 'uploaded_at', 'summary_json']
        read_only_fields = ['id', 'uploaded_at', 'summary_json']
    
    def validate_file(self, value):
        """
        Validate CSV file extension and size.
        """
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError(
                "Only CSV files are allowed."
            )
        
        # Check file size (10MB max)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError(
                "File size must not exceed 10MB."
            )
        
        return value


class AnalyticsSummarySerializer(serializers.Serializer):
    """
    Serializer for analytics summary response.
    
    Returns computed statistics from the most recent dataset.
    """
    
    total_equipment = serializers.IntegerField(
        help_text='Total number of equipment entries'
    )
    average_flowrate = serializers.FloatField(
        help_text='Average flowrate across all equipment'
    )
    average_pressure = serializers.FloatField(
        help_text='Average pressure across all equipment'
    )
    average_temperature = serializers.FloatField(
        help_text='Average temperature across all equipment'
    )


class EquipmentDistributionSerializer(serializers.Serializer):
    """
    Serializer for equipment type distribution.
    
    Returns count of each equipment type.
    """
    
    type = serializers.CharField(help_text='Equipment type name')
    count = serializers.IntegerField(help_text='Number of equipment of this type')


class HistorySerializer(serializers.ModelSerializer):
    """
    Serializer for dataset upload history.
    
    Returns basic information about past uploads.
    """
    
    class Meta:
        model = DatasetUpload
        fields = ['id', 'file', 'uploaded_at']
        read_only_fields = ['id', 'file', 'uploaded_at']
