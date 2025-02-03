from django.contrib import admin
from .models.receipt import ReceiptImage  # Correct import path

@admin.register(ReceiptImage)
class ReceiptImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_at')