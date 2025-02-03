from rest_framework import serializers
from receipts.models.receipt import ReceiptImage

class ReceiptImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptImage
        fields = ['image']