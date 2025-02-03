from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from receipts.models.receipt import ReceiptImage
from receipts.serializers.receipt import ReceiptImageSerializer

class ReceiptUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = ReceiptImageSerializer(data=request.data)
        if serializer.is_valid():
            receipt = serializer.save()
            return Response({
                'id': receipt.id,
                'status': 'uploaded',
                'message': 'File uploaded successfully',
                'image_url': request.build_absolute_uri(receipt.image.url)
            })
        return Response(serializer.errors, status=400)