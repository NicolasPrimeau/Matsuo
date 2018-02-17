from matsuo.service_base.service import Service
import boto3
from PIL import Image
import os
import regex as re


class DescribeService(Service):

    bucket_name='uottahack18'
    ACCESS_ID = 'AKIAJAO4JDKXZG6QMNNQ'
    ACCESS_KEY = 'iVBQrlRUm4D6pF4GE6LwC7p/tyZgw3g4LOCM64Ux'
    SERVICE_NAME = 'DescribeService'

    def __init__(self, **kwargs):
        super().__init__(DescribeService.SERVICE_NAME, kwargs)

    def start(self):
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
