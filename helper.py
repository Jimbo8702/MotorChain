import requests
import os
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from PIL import Image
import io
from pathlib import Path

pinataurl = "https://api.pinata.cloud/pinning/pinFileToIPFS"
pinata_secret = "485ba80bbf135a8541e61f085ade21817928049b15261b101a3626c325b0765c"
pinata_public = "e62cd9c7fe0d2c11c083"


def upload_file(file_path_to_upload, name):
    fileName = name
    m = MultipartEncoder(
        fields={
            "file": (fileName, open(file_path_to_upload, "rb")),
        }
    )

    headers = {
        "pinata_api_key": pinata_public,
        "pinata_secret_api_key": pinata_secret,
        "Content-Type": m.content_type,
    }

    r = requests.post(pinataurl, data=m, headers=headers)

    if r.status_code == 200:
        print("file_uploaded")
        print(r.json()["IpfsHash"])
    else:
        print(r._content)


def upload_image(image_path, name):
    with Path(image_path).open("rb") as fp:
        file_binary = fp.read()

    imageName = name + "_image"
    m = MultipartEncoder(
        fields={
            "file": (imageName, file_binary),
        }
    )

    headers = {
        "pinata_api_key": pinata_public,
        "pinata_secret_api_key": pinata_secret,
        "Content-Type": m.content_type,
    }

    r = requests.post(pinataurl, data=m, headers=headers)

    if r.status_code == 200:
        print("image_uploaded")
        print(r.json())
        return r.json()["IpfsHash"]
    else:
        print(r._content)


def write_file(context, image):
    name = context["name"]
    imageStream = io.BytesIO(image.getvalue())
    imageFile = Image.open(imageStream)
    imageFile.save(f"./cars/{name}.jpeg")
    ipfs_img_hash = upload_image(f"./cars/{name}.jpeg", name=name)
    if ipfs_img_hash:
        context["image"] = "ipfs://" + ipfs_img_hash + f"/{name}_image.jpeg"
        json_object = json.dumps(context, indent=4)
        with open(f"./cars/{name}.json", "w") as outfile:
            outfile.write(json_object)
        upload_file(
            file_path_to_upload=f"./cars/{name}.json",
            name=name,
        )
