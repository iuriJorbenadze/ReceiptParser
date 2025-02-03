from rest_framework import serializers
from receipts.models.receipt import ReceiptImage

class ReceiptImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        style={'input_type': 'file'},
        help_text='Upload receipt image'
    )

    class Meta:
        model = ReceiptImage
        fields = ['image']