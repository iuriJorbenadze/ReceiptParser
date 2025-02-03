from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from receipts.views.receipt import ReceiptUploadView  # Make sure this import exists

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/receipts/upload/', ReceiptUploadView.as_view(), name='receipt-upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)