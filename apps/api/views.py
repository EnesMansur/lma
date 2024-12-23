from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(self, data=None, message="ok", status_code=200, total_page=None, **kwargs):
        result = False
        if 200 <= status_code < 300:
            result = True

        if result:
            response_data = {
                "result": result,
                "message": message,
                "data": data
            }
            if total_page is not None:
                response_data["total_page"] = total_page
        else:
            response_data = {
                "result": result,
                "message": message,
                "data": None
            }
        super().__init__(response_data, status=status_code, **kwargs)
