from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError

class CompanyUser(AbstractUser):
    USER_TYPES = (
        ('Ops', 'Operations'),
        ('Client', 'Client'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='Client')
    email_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class File(models.Model):
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='uploaded_files')
    file_type = models.CharField(max_length=10, choices=[('pptx', 'PPTX'), ('docx', 'DOCX'), ('xlsx', 'XLSX')])
    file = models.FileField(upload_to='uploaded_files/')
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

    def clean(self):
        if self.file_type not in ['pptx', 'docx', 'xlsx']:
            raise ValidationError('Invalid file type.')

    def generate_secure_url(self):
        return f"/download-file/{self.id}"

    def is_accessible_by(self, user):
        return user.user_type == 'Client'
