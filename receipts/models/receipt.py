from django.db import models

class ReceiptImage(models.Model):
    def upload_to(instance, filename):
        """Generate unique filename for each upload"""
        import uuid
        ext = filename.split('.')[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"
        return f"receipts/{filename}"

    image = models.ImageField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_data = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')