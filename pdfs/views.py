# pdfs/views.py
from datetime import timedelta
import json

import boto3
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
import requests
from rest_framework import status
from rest_framework.views import APIView

from orders.models import Order
from utils.aws_utils import upload_file
from utils.pdf_utils import create_pdf
from utils.utils import standard_response
from .models import PresignedURL


class GenerateUploadPDFView(APIView):
    def post(self, request):
        try:
            order_id = request.data.get('order_id')
            if not order_id:
                return standard_response(False, "order_id is required", status_code=status.HTTP_400_BAD_REQUEST)

            # Fetch the order details
            order = get_object_or_404(Order, id=order_id)
            customer_name = order.customer.name
            contact_number = order.customer.phone_number
            pdf_data = [(item.quantity, item.product.name) for item in order.items.all()]
            pdf_buffer = create_pdf(pdf_data, customer_name, contact_number, order_id)

            # Upload the PDF to S3
            s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
            pdf_filename = f'order_note_{order_id}.pdf'
            upload_success = upload_file(pdf_buffer, s3_bucket, pdf_filename)
            if not upload_success:
                return standard_response(False, "Failed to upload PDF",
                                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return standard_response(True, "PDF generated and uploaded")
        except Exception as e:
            return standard_response(False, str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SendWhatsAppMessageView(APIView):
    def post(self, request):
        try:
            order_id = request.data.get('order_id')
            if not order_id:
                return standard_response(False, "order_id is required",
                                         status_code=status.HTTP_400_BAD_REQUEST)

            presigned_url_obj = get_object_or_404(PresignedURL, order_id=order_id)
            presigned_url = presigned_url_obj.url

            order = get_object_or_404(Order, id=order_id)
            order_number = order.id
            generated_at = order.created_at.strftime("%Y-%m-%d %H:%M:%S")

            whatsapp_url = settings.WHATSAPP_API_URL
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {settings.WHATSAPP_API_TOKEN}'
            }

            payload_pdf = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": f'{settings.WHATSAPP_PHONE_NUMBER}',
                "type": "template",
                "template": {
                    "name": "order_note_1",
                    "language": {"code": "en_US"},
                    "components": [
                        {
                            "type": "body",
                            "parameters": [
                                {"type": "text", "text": str(order_number)},
                                {"type": "text", "text": generated_at},
                            ]
                        },
                        {
                            "type": "header",
                            "parameters": [
                                {
                                    "type": "document",
                                    "document": {
                                        "link": presigned_url,
                                        "filename": f"order_note_{order_id}.pdf"
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
            response_pdf = requests.post(whatsapp_url, headers=headers, data=json.dumps(payload_pdf))

            if response_pdf.status_code != 200:
                return standard_response(False, "Failed to send PDF", error=response_pdf.text,
                                         status_code=response_pdf.status_code)

            return standard_response(True, "PDF sent via WhatsApp")

        except Exception as e:
            return standard_response(False, str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GeneratePresignedURLView(APIView):
    def post(self, request):
        try:
            order_id = request.data.get('order_id')
            if not order_id:
                return standard_response(False, "order_id is required", status_code=status.HTTP_400_BAD_REQUEST)

            order = get_object_or_404(Order, id=order_id)

            s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
            pdf_filename = f'order_note_{order_id}.pdf'
            expiration = int(settings.AWS_PRESIGNED_URL_EXPIRATION)
            s3_client = boto3.client('s3')
            presigned_url = s3_client.generate_presigned_url('get_object',
                                                             Params={'Bucket': s3_bucket,
                                                                     'Key': pdf_filename},
                                                             ExpiresIn=expiration)

            expiry_time = timezone.now() + timedelta(seconds=expiration)
            presigned_url_obj, created = PresignedURL.objects.get_or_create(order=order)
            presigned_url_obj.url = presigned_url
            presigned_url_obj.expiry_time = expiry_time
            presigned_url_obj.save()

            return standard_response(True, "Presigned URL generated successfully", presigned_url)

        except Exception as e:
            return standard_response(False, str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
