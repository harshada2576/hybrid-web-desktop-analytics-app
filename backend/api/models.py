"""
Database models for IIT Bombay Analytics Backend.

Models:
    - DatasetUpload: Stores CSV uploads with computed analytics summary
"""

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_csv_file(file):
    """
    Validate that uploaded file is a CSV.
    
    Args:
        file: Uploaded file object
        
    Raises:
        ValidationError: If file is not a CSV
    """
    if not file.name.endswith('.csv'):
        raise ValidationError('Only CSV files are allowed.')


class DatasetUpload(models.Model):
    """
    Model to store CSV dataset uploads with analytics summary.
    
    Automatically maintains only the last 5 uploads by deleting
    the oldest record when a new one is created.
    
    Attributes:
        file: The uploaded CSV file
        uploaded_at: Timestamp of upload
        summary_json: JSON field containing computed analytics (equipment count,
                     averages, type distribution)
        user: User who uploaded the dataset (optional for future multi-user support)
    """
    
    file = models.FileField(
        upload_to='datasets/',
        validators=[validate_csv_file],
        help_text='CSV file containing equipment data'
    )
    
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when the dataset was uploaded'
    )
    
    summary_json = models.JSONField(
        default=dict,
        blank=True,
        help_text='Computed analytics summary stored as JSON'
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='datasets',
        null=True,
        blank=True,
        help_text='User who uploaded the dataset'
    )
    
    class Meta:
        ordering = ['-uploaded_at']  # Most recent first
        verbose_name = 'Dataset Upload'
        verbose_name_plural = 'Dataset Uploads'
    
    def __str__(self):
        return f"Dataset uploaded at {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def save(self, *args, **kwargs):
        """
        Override save to enforce 5-upload limit.
        
        Before saving a new upload, checks if 5 records already exist.
        If so, deletes the oldest one to maintain the limit.
        """
        # Check if we need to delete old uploads (keep only last 5)
        max_uploads = getattr(settings, 'MAX_DATASET_HISTORY', 5)
        
        # Only enforce limit for new records (not updates)
        if not self.pk:
            # Count existing uploads for this user
            existing_count = DatasetUpload.objects.filter(
                user=self.user
            ).count()
            
            if existing_count >= max_uploads:
                # Delete the oldest upload(s) to make room
                uploads_to_delete = DatasetUpload.objects.filter(
                    user=self.user
                ).order_by('uploaded_at')[:(existing_count - max_uploads + 1)]
                
                for upload in uploads_to_delete:
                    # Delete the file from storage
                    if upload.file:
                        upload.file.delete(save=False)
                    upload.delete()
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """
        Override delete to also remove the file from storage.
        """
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)
