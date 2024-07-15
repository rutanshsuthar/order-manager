from rest_framework import status
from rest_framework.response import Response
import time


def standard_response(success, message, data=None, error=None, status_code=status.HTTP_200_OK):
    # time.sleep(6)
    response = {
        "success": success,
        "message": message,
        "data": data,
        "error": error
    }
    return Response(response, status=status_code)
