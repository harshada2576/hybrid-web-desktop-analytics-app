"""
API Views for IIT Bombay Analytics Backend.

This module contains all API endpoint implementations.
Views are kept thin - business logic is delegated to services.

Endpoints:
    Authentication:
        - POST /api/auth/register/
        - POST /api/auth/login/
        - POST /api/auth/logout/
    
    Data:
        - POST /api/upload/
        - GET /api/summary/
        - GET /api/distribution/
        - GET /api/history/
"""

import os
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import DatasetUpload
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    DatasetUploadSerializer,
    AnalyticsSummarySerializer,
    EquipmentDistributionSerializer,
    HistorySerializer
)
from .services.analytics import (
    compute_summary_statistics,
    get_equipment_distribution,
    CSVValidationError
)
from .services.pdf_generator import generate_analytics_report
from django.http import HttpResponse


# ================================
# AUTHENTICATION ENDPOINTS
# ================================

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user account.
    
    Endpoint: POST /api/auth/register/
    
    Request body:
        - username (string, required)
        - email (string, required)
        - password (string, required)
        - password_confirm (string, required)
    
    Returns:
        201: User created successfully with auth token
        400: Validation errors
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate authentication token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Registration failed',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Authenticate user and return auth token.
    
    Endpoint: POST /api/auth/login/
    
    Request body:
        - username (string, required)
        - password (string, required)
    
    Returns:
        200: Login successful with auth token
        400: Invalid credentials or validation errors
    """
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Get or create token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'token': token.key
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials',
                'details': 'Username or password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'error': 'Validation failed',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout user by deleting their auth token.
    
    Endpoint: POST /api/auth/logout/
    
    Headers:
        - Authorization: Token <token>
    
    Returns:
        200: Logout successful
    """
    try:
        # Delete the user's token
        request.user.auth_token.delete()
        
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': 'Logout failed',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


# ================================
# DATA HANDLING ENDPOINTS
# ================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_dataset(request):
    """
    Upload and validate CSV dataset.
    
    Endpoint: POST /api/upload/
    
    Headers:
        - Authorization: Token <token>
    
    Request body (multipart/form-data):
        - file (CSV file, required)
    
    CSV must contain:
        - Equipment Name
        - Type
        - Flowrate (numeric)
        - Pressure (numeric)
        - Temperature (numeric)
    
    Returns:
        201: Upload successful with computed summary
        400: Validation errors or invalid CSV format
    """
    serializer = DatasetUploadSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            # Save the upload (this will handle 5-upload limit automatically)
            dataset = serializer.save(user=request.user)
            
            # Get file path
            file_path = dataset.file.path
            
            # Compute analytics using service layer
            summary = compute_summary_statistics(file_path)
            
            # Store summary in model
            dataset.summary_json = summary
            dataset.save()
            
            return Response({
                'message': 'Dataset uploaded successfully',
                'dataset': {
                    'id': dataset.id,
                    'uploaded_at': dataset.uploaded_at,
                    'summary': summary
                }
            }, status=status.HTTP_201_CREATED)
            
        except CSVValidationError as e:
            # Delete the uploaded file if validation fails
            if hasattr(dataset, 'file') and dataset.file:
                dataset.file.delete()
                dataset.delete()
            
            return Response({
                'error': 'CSV validation failed',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Clean up on unexpected errors
            if 'dataset' in locals() and hasattr(dataset, 'file'):
                dataset.file.delete()
                dataset.delete()
            
            return Response({
                'error': 'Upload failed',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'error': 'Validation failed',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request):
    """
    Get analytics summary from the most recent dataset.
    
    Endpoint: GET /api/summary/
    
    Headers:
        - Authorization: Token <token>
    
    Returns:
        200: Summary statistics
        404: No datasets found
    """
    try:
        # Get the most recent dataset for this user
        dataset = DatasetUpload.objects.filter(user=request.user).first()
        
        if not dataset:
            return Response({
                'error': 'No datasets found',
                'details': 'Please upload a dataset first'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Return stored summary
        return Response({
            'total_equipment': dataset.summary_json.get('total_equipment', 0),
            'average_flowrate': dataset.summary_json.get('average_flowrate', 0),
            'average_pressure': dataset.summary_json.get('average_pressure', 0),
            'average_temperature': dataset.summary_json.get('average_temperature', 0)
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': 'Failed to retrieve summary',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_distribution(request):
    """
    Get equipment type distribution from the most recent dataset.
    
    Endpoint: GET /api/distribution/
    
    Headers:
        - Authorization: Token <token>
    
    Returns:
        200: Equipment type distribution
        404: No datasets found
    """
    try:
        # Get the most recent dataset for this user
        dataset = DatasetUpload.objects.filter(user=request.user).first()
        
        if not dataset:
            return Response({
                'error': 'No datasets found',
                'details': 'Please upload a dataset first'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Return equipment distribution from stored summary
        distribution = dataset.summary_json.get('equipment_distribution', [])
        
        return Response({
            'distribution': distribution
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': 'Failed to retrieve distribution',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    """
    Get upload history (last 5 uploads).
    
    Endpoint: GET /api/history/
    
    Headers:
        - Authorization: Token <token>
    
    Returns:
        200: List of past uploads
    """
    try:
        # Get all datasets for this user (already limited to 5 by model)
        datasets = DatasetUpload.objects.filter(user=request.user)
        
        serializer = HistorySerializer(datasets, many=True)
        
        return Response({
            'history': serializer.data
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': 'Failed to retrieve history',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf_report(request):
    """
    Generate and download PDF analytical report.
    
    Endpoint: GET /api/report/pdf/
    
    Headers:
        - Authorization: Token <token>
    
    Returns:
        200: PDF file download
        404: No datasets found
        400: PDF generation error
    """
    try:
        # Get the most recent dataset for this user
        dataset = DatasetUpload.objects.filter(user=request.user).first()
        
        if not dataset:
            return Response({
                'error': 'No datasets found',
                'details': 'Please upload a dataset first'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Extract filename from uploaded file path
        import os
        dataset_filename = os.path.basename(dataset.file.name)
        
        # Get summary and distribution data
        summary = dataset.summary_json
        distribution = summary.get('equipment_distribution', [])
        
        # Generate PDF
        pdf_buffer = generate_analytics_report(
            dataset_filename=dataset_filename,
            upload_timestamp=dataset.uploaded_at.isoformat(),
            summary=summary,
            distribution=distribution
        )
        
        # Create HTTP response with PDF
        response = HttpResponse(
            pdf_buffer.getvalue(),
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename="equipment_analytics_report.pdf"'
        
        return response
    
    except Exception as e:
        return Response({
            'error': 'Failed to generate PDF report',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
