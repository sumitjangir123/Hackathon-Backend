from bson import ObjectId
from fastapi.param_functions import Query
from pydantic import BaseModel, Field, EmailStr, fields
from typing import Dict, Optional, List
from fastapi import File, UploadFile
from datetime import datetime

class SchemalessResponse(BaseModel):
    message:str
    success:bool
    obj: Optional[dict] = None