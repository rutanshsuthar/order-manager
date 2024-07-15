# pdfs/urls.py
from django.urls import path

from .views import GeneratePresignedURLView, GenerateUploadPDFView, SendWhatsAppMessageView

urlpatterns = [
    path('generate-upload-pdf/', GenerateUploadPDFView.as_view(), name='generate_upload_pdf'),
    path('generate-presigned-url/', GeneratePresignedURLView.as_view(), name='generate_presigned_url'),
    path('send-whatsapp-message/', SendWhatsAppMessageView.as_view(), name='send_whatsapp_message'),
]
