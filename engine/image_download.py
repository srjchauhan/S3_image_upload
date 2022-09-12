import pprint
import shutil

import requests
import os
from config import PathConfig


def download_image(url, name):
    temp_path = PathConfig.temp_path
    ext = os.path.splitext(url)[-1]
    file_path = os.path.join(temp_path, name + ext)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        return True, name + ext
    else:
        return False, r.reason


if __name__ == "__main__":
    image_url = "https://cdn.pixabay.com/photo/2020/02/06/09/39/summer-4823612_960_720.jpg"
    download_image(image_url, "asd")
