from matsuo.service_base.service import HostedService
import boto3
import os
import regex as re

bucket_name = 'uottahack18'
ACCESS_ID = 'AKIAJAO4JDKXZG6QMNNQ'
ACCESS_KEY = 'iVBQrlRUm4D6pF4GE6LwC7p/tyZgw3g4LOCM64Ux'


def get_keywords(args):
    filename = args['data']
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


class DescribeService(HostedService):
    SERVICE_NAME = 'Describe'

    def __init__(self, **kwargs):
        super().__init__(DescribeService.SERVICE_NAME, kwargs=kwargs)

    def start(self):
        self.host.add_endpoint('get_keywords', 'get_keywords', get_keywords, methods=['GET'])
        self.host.start()


class FileSizeLimitExceededError(LookupError):
    '''Files must be less that 5MB'''
