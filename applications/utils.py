import imp
from applications.schema import SchemalessResponse
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from bson.objectid import ObjectId


from fastapi.encoders import jsonable_encoder
from datetime import datetime,timedelta
from typing import Dict, Optional, List
import requests

def make_standard_response(**kwargs):
    message = kwargs.get("message") if kwargs.get("message") else None
    success = kwargs.get("success") if kwargs.get("success") else True
    obj = kwargs.get("obj") if kwargs.get("obj") else None
    status_code = kwargs.get("status_code") if kwargs.get("status_code") else status.HTTP_200_OK
    
    response = SchemalessResponse(
                message=str(message),
                success=success,
                obj = obj
            )

    print (response)
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(response)
    )