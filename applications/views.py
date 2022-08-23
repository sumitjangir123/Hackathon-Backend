import csv
import imp
import io
import os
from sre_constants import SUCCESS
import zipfile
from starlette.requests import Request

from config import Config
from .utils import make_standard_response
from fastapi.param_functions import Body
from starlette import status
from fastapi.encoders import jsonable_encoder 
from datetime import timedelta, datetime
from fastapi import APIRouter, status, Form, Body, Depends, File, UploadFile, Response
from fastapi.responses import FileResponse
from applications.schema import SchemalessResponse
import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from pathlib import Path

class product: 
    def __init__(self, id, name, desc, price, imageUrl, division): 
        self.id = id
        self.name = name
        self.desc = desc
        self.price = price
        self.imageUrl = imageUrl 
        self.division = division


import requests
from requests.auth import HTTPBasicAuth



router = APIRouter()

# def zipfiles(filenames):
#     zip_filename = "archive.zip"

#     s = io.BytesIO()
#     zf = zipfile.ZipFile(s, "w")

#     for fpath in filenames:
#         # Calculate path for file in zip
#         fdir, fname = os.path.split(fpath[1])
#         print(fname)
#         # Add file, at correct path
#         zf.write(fpath[1], fname)

#     # Must close zip for all contents to be written
#     zf.close()

#     print(zf)
#     # Grab ZIP file from in-memory, make response with correct MIME-type
#     resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
#         'Content-Disposition': f'attachment;filename={zip_filename}'
#     })

#     return resp

# Read image features
fe = FeatureExtractor()
features = []
img_paths = []

for feature_path in Path("./static/feature").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/img") / (feature_path.stem + ".jpg"))
features = np.array(features)


@router.post('/upload_file', response_description="upload file to get simmilar results")
async def upload_file(file: UploadFile = File(...)):
    request_object_content = await file.read()
    # Save query image
    img = Image.open(io.BytesIO(request_object_content))  # PIL image
    uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":",
                                                                                ".") + "_" + file.filename
    img.save(uploaded_img_path)

    # Run search
    query = fe.extract(img)
    # L2 distances to features
    dists = np.linalg.norm(features-query, axis=1)
    ids = np.argsort(dists)[:1]  # Top 30 results
    scores = [(dists[id], img_paths[id]) for id in ids]

    # fdir, fname = os.path.split(scores[0][1])
    # print(fdir)
    # print(type(scores))
    # zipfiles(scores)
    
    # print(scores)

    temp = []
    for item in scores:
        with open('./static/styles.csv', 'r') as file:
            csvreader = csv.reader(file)
            fdir, fname = os.path.split(item[1]) #15177
            for row in csvreader:
                if (fname.split('.')[0] in row):
                    temp.append(row)

    print(temp)

    URL = "https://stage.api.azeus.gaptech.com/commerce/search/products/v2/style?keyword=" + temp[0][1] +" "+temp[0][4]+ " " +temp[0][5]

    headers = {'Accept': 'application/json','apikey':Config.apikey}

    req = requests.get(URL, headers=headers)
    result = req.json()

    
    # print("The pastebin URL is:%s"%pastebin_url)



    response_list = [] #list
    # response_list.append(product('temp', "temp", "temp", "temmp","temp","temp" ))  
    

    for index,state in enumerate(result["products"]):
        if(index>10):break
        # print(state['id'])
        for data in state["colors"]:
            if temp[0][5] in data["name"]:
                file_path = "https://www.gap.com"+data['images'][0]['path']
                response_list.append(product(state['id'], state['name'], state['description'], data['regularPrice'],file_path,state['webProductType'] ))
                

     
    print(response_list)
    

    return make_standard_response(
        obj = dict(product=response_list),
        message=str(len(scores) )+ " Results fetched successfully",
        status_code=200,
        success="true"
    )
    # return zipfiles(scores)
    # return "(query_path=uploaded_img_path,scores=scores)"
