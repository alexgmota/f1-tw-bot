from twitter import *
import json

def getConnection():
    credentials = getCredentials()
    t = Twitter(
        auth=OAuth(
            credentials["access_token"],
            credentials["access_token_secret"],
            credentials["key"],
            credentials["key_secret"],
        )
    )
    print("Connection created")
    return t

def getUploadConnection():
    credentials = getCredentials()
    return Twitter(
        domain="upload.twitter.com",
        auth=OAuth(
            credentials["access_token"],
            credentials["access_token_secret"],
            credentials["key"],
            credentials["key_secret"],
        ),
    )

def getCredentials():
    with open("credentials.json") as file:
        return json.load(file)

def postTextTweet(msg):
    t = getConnection()
    t.statuses.update(status=msg)
    print("Message sent")
    print("Message content:\n" + msg)

def postImageTweet(msg, images):
    t = getConnection()
    t_upload = getUploadConnection()
    imgIdArr = []
    for img in images:
        with open(img, "rb") as imagefile:
            imagedata = imagefile.read()
        imgIdArr.append(t_upload.media.upload(media=imagedata)["media_id_string"])

    t.statuses.update(status=msg, media_ids=",".join(imgIdArr))
    print("Message sent")
    print("Message content:\n" + msg)
    print(images)
