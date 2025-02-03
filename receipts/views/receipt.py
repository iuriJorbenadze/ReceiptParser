from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from receipts.models.receipt import ReceiptImage
from receipts.serializers.receipt import ReceiptImageSerializer

class ReceiptUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request):
        # This enables proper form rendering
        serializer = ReceiptImageSerializer()
        return Response({
            'description': 'Upload a receipt image',
            'form': serializer.data
        })

    def post(self, request):
        serializer = ReceiptImageSerializer(data=request.data)
        if serializer.is_valid():
            receipt = serializer.save()
            return Response({
                'id': receipt.id,
                'status': 'uploaded',
                'image_url': request.build_absolute_uri(receipt.image.url)
            })
        return Response(serializer.errors, status=400)