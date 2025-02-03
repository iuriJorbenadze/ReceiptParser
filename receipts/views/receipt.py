from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from receipts.models.receipt import ReceiptImage
from receipts.serializers.receipt import ReceiptImageSerializer
from receipts.services.receipt_processor import process_receipt_image  # Add this import

class ReceiptUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request):
        serializer = ReceiptImageSerializer()
        return Response({
            'description': 'Upload a receipt image',
            'form': serializer.data
        })

    def post(self, request):
        serializer = ReceiptImageSerializer(data=request.data)
        if serializer.is_valid():
            receipt = serializer.save()

            try:
                # Process the image immediately after upload
                processed_data = process_receipt_image(receipt.image.path)

                # Update the receipt with processed data
                receipt.processed_data = processed_data
                receipt.status = 'completed'
                receipt.save()

                return Response({
                    'id': receipt.id,
                    'status': receipt.status,
                    'image_url': request.build_absolute_uri(receipt.image.url),
                    'processed_data': processed_data
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                # Handle processing errors
                receipt.status = 'failed'
                receipt.save()
                return Response({
                    'error': str(e),
                    'status': 'failed',
                    'receipt_id': receipt.id
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)