import pprint
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import uvicorn
from engine import download_image, s3_client
import os
from pydantic import BaseModel
from config import PathConfig


class Item(BaseModel):
    image_url: str
    image_name: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health():
    return {"message": "Success"}


@app.post("/upload/")
def upload(request: Item):
    response = {
        'status': '',
        'error': ''
    }
    try:
        url, name = request.image_url, request.image_name
        url = url.split('?')[0]
        status, file_name = download_image(url=url, name=name)
        if status:
            s3 = s3_client()
            if s3.check_file_exist(filename=file_name):
                response['status'] = 'Error '
                response['error'] = f'FILE EXIst: File with name {name} already exist in bucket'
                os.remove(os.path.join(PathConfig.temp_path, file_name))
                return response
            upload_status, resp = s3.upload_image(name=file_name)
            if upload_status:

                response['status'] = 'Success'
                response['error'] = ''
            else:
                response['status'] = 'Error '
                response['error'] = 'Unable to upload image to s3' + resp
            os.remove(os.path.join(PathConfig.temp_path, file_name))
        else:
            response['status'] = 'Error'
            response['error'] = 'Unable to download image' + file_name

    except Exception as e:
        response['status'] = 'Error'
        response['error'] = str(e)

    finally:
        return response


@app.get("/list_file")
def list_file():
    response = {
        'status': '',
        'image_list': [],
        'error': ''
    }
    try:
        s3 = s3_client()
        status, img_list = s3.list_images()
        if status:
            response['status'] = 'Success'
            response['image_list'] = img_list
        else:
            response['status'] = 'Error'
            response['error'] = 'Unable to get image list from s3 ' + img_list

    except Exception as e:
        response['status'] = 'Error'
        response['error'] = str(e)
    finally:
        return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
