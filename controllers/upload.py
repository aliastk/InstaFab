""" Adapted from https://bitbucket.org/luca_de_alfaro/web2py_start_2016/src/f1f53c41f65ffa3b1cd5aa6a772d1d2db5d290b2/controllers/uploader.py?at=luca-gcs-uploads&fileviewer=file-view-default
and repurposed for our app """


import base64
import json
import os
import time
import urllib
import boto3

from gluon.utils import web2py_uuid
from gluon import current

priv_folder = os.path.join(current.request.folder, 'private')
key_file = os.path.join(priv_folder, 'S3.json')
AWS_KEY_INFO = json.load(open(key_file))
session = boto3.session.Session(aws_access_key_id=AWS_KEY_INFO['key_id'],aws_secret_access_key=AWS_KEY_INFO['access_key'])
client = session.client('s3')

def aws_url(Method,key=None,expiration=3600):

    # TODO: make a seperate handler
    if(Method=='get_object'):
        signed_url = client.generate_presigned_url(
            ClientMethod=Method,
            Params={
                'Bucket': 'instafabpictures',
                'Key': key,
                'ResponseContentType':'image/png'
            },
            ExpiresIn=expiration
        )
        return signed_url

    signed_url = client.generate_presigned_url(
        ClientMethod=Method,
        Params={
            'Bucket': 'instafabpictures',
            'Key': key,
            'ContentType':'image/png'
        },
        ExpiresIn=expiration
    )
    return signed_url


def get_upload_url():
    """Returns a fresh URL with ID to post something to GCS.
    It returns a dictionary with two fields:
    - upload_url: used for uploading
    - download_url: used for retrieving the content"""
    # Invents a random name for the image.
    image_path = web2py_uuid() + ".png"
    signed_put_url=aws_url('put_object',key=image_path,expiration=3600*24*365*15)
    #signed_get_url = gcs_url(image_path, verb='GET',
    #                         expiration_secs=3600 * 24 * 365 * 50)
    # This line is required; otherwise, cross-domain requests are not accepted.
    #response.headers['Access-Control-Allow-Origin'] = '*'
    return response.json(dict(
        signed_url=signed_put_url,
        image_path=image_path
        #access_url=signed_get_url
    ))

def get_download_url():
    """Returns a fresh URL with ID to post something to GCS.
    It returns a dictionary with two fields:
    - upload_url: used for uploading
    - download_url: used for retrieving the content"""
    # Invents a random name for the image.
    get_url=aws_url('get_object',key=request.vars.image_path,expiration=3600*24*365*15)
    #signed_get_url = gcs_url(image_path, verb='GET',
    #                         expiration_secs=3600 * 24 * 365 * 50)
    # This line is required; otherwise, cross-domain requests are not accepted.
    #response.headers['Access-Control-Allow-Origin'] = '*'
    return response.json(dict(
        get_url=get_url,
        #access_url=signed_get_url
    ))

def add():
    import datetime
    if(request.vars.shopping is not None and sendlink(request.vars.shopping) == "unsafe"):
        return "unsafe"

    if "//" not in request.vars.shopping:
        request.vars.shopping = "//"+request.vars.shopping
    post = db.Posts.insert(
        PictureUrl = request.vars.picture,
        MyMessage = request.vars.MyMessage,
        CreatedOn = datetime.datetime.utcnow(),
        Tags = request.vars.Tags,
        rating = 50.0,
        Recency = datetime.datetime.now(),
        search_rating = 50.0,
        search_recency = datetime.datetime.now(),
        Shopping = request.vars.shopping
    )
    return "ok"

def check():
    return sendlink(request.vars.link)

def sendlink(link):
    import safebrowsing
    import json
    apikey = myconf.get('lookup.key')
    sb = safebrowsing.LookupAPI(apikey)
    resp = sb.threat_matches_find(link)
    if u'matches' in resp:
        return "unsafe"
    return "ok"
