import boto3
import os
import regex as re

bucket_name='uottahack18'
ACCESS_ID = 'AKIAI5AFWS4QZ7DHKZBA'
ACCESS_KEY = 'DVZzDCEGjgznb3aoW//PyTYtb18zfhv3tv5SRhfA'

def get_keywords(filename):
    size = os.path.getsize(filename)
    if(size>5*2**20):
        raise FileSizeLimitExceededError(filename)
    client = boto3.client('rekognition',region_name='us-east-1',aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY)
    with open(filename,'rb') as imgb:
        img = imgb.read()
        details = {'Bytes':img}
    response = client.detect_labels(Image=details,MaxLabels=10,MinConfidence=60)
    sresponse = sorted(response['Labels'], key=lambda k: k['Confidence'])
    keywords = []
    for item in response['Labels']:
        keywords.append(item['Name'])
    print(keywords)
    return keywords

class FileSizeLimitExceededError(LookupError):
    '''Files must be less that 5MB'''

get_keywords("./lifeboat.jpg")

#to bucket:
# s3 = boto3.resource('s3',aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY)
# name = re.sub(r'(/)[a-zA-Z0-9]*(/)','',filename, flags=re.I)
# name = re.sub(r'(\./)','', name)
# s3.Bucket(bucket_name).put_object(Key=name, Body=img64)
# details = {'S3Object':{'Bucket':bucket_name}}
