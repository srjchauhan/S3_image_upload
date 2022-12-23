# S3_image_upload
AN API based Application for uploading images from web links to AWS S3 bucket

## The Steps to set up on local 
### Git clone the repo
```
git@github.com:srjchauhan/S3_image_upload.git
```
This should clone all the files in a directory called S3_image_upload.

Go to  project directory:
```
cd S3_image_upload/
```


create venv
```
python -m venv venv
```
activate virtual environment
```
source venv/bin/activate
```
Install dependencies with 

```
pip install -r requirements.txt
```

create env variable and fill in respective env value 
```
AWS_ACCESS_ID=
AWS_ACCESS_KEY=
REGION_NAME=
BUCKET_NAME=
BUCKET_DIR=
TEMP_DIR=.sys-cache
```
## Run app

```
python main.py
```

## Access swagger UI 
```
localhost:8000/docs
```