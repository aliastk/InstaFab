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
    """Generates a GCS path
    Given a path on GCS and an expiration_secs (seconds) it generates a signed URL valid for that
    number of seconds. keytext and gae_app and inferred from the environment, pass only to override
    gae_app is necessary when running locally and server_utils is not available.
    """
    signed_url = client.generate_presigned_url(
        ClientMethod=Method,
        Params={
            'Bucket': 'instafabpictures',
            'Key': key,
            'ContentType':'image/jpeg'
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
    image_path = web2py_uuid() + ".jpeg"
    signed_put_url=aws_url('put_object',key=image_path,expiration=3600*24*365*15)
    #signed_get_url = gcs_url(image_path, verb='GET',
    #                         expiration_secs=3600 * 24 * 365 * 50)
    # This line is required; otherwise, cross-domain requests are not accepted.
    #response.headers['Access-Control-Allow-Origin'] = '*'
    return response.json(dict(
        signed_url=signed_put_url,
        #access_url=signed_get_url
    ))
