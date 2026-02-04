"""
Admin configuration for API models.
"""

from django.contrib import admin
from .models import DatasetUpload


@admin.register(DatasetUpload)
class DatasetUploadAdmin(admin.ModelAdmin):
    """
    Admin interface for DatasetUpload model.
    """
    list_display = ['id', 'user', 'file', 'uploaded_at']
    list_filter = ['uploaded_at', 'user']
    search_fields = ['user__username']
    readonly_fields = ['uploaded_at', 'summary_json']
    
    def has_add_permission(self, request):
        """Prevent manual additions through admin - uploads should go through API."""
        return False
