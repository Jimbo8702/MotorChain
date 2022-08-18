import requests
import os
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from io import StringIO

pinataurl = "https://api.pinata.cloud/pinning/pinFileToIPFS"
pinata_secret = "485ba80bbf135a8541e61f085ade21817928049b15261b101a3626c325b0765c"
pinata_public = "e62cd9c7fe0d2c11c083"


def upload(file_path_to_upload, image, name):
    fileName = name
    m = MultipartEncoder(
        fields={
            "file": [
                (fileName, open(file_path_to_upload, "rb")),
                (fileName, open(image, "rb")),
            ]
        }
    )

    headers = {
        "pinata_api_key": pinata_public,
        "pinata_secret_api_key": pinata_secret,
        "Content-Type": m.content_type,
    }

    r = requests.post(pinataurl, data=m, headers=headers)

    if r.status_code == 200:
        print(r.json()["IpfsHash"])
    else:
        print(r._content)


def write_file(context, image):
    json_object = json.dumps(context, indent=4)
    name = context["name"]
    with open(f"./cars/{name}.json", "w") as outfile:
        outfile.write(json_object)
    upload(f"./cars/{name}.json", image=image, name=name)
