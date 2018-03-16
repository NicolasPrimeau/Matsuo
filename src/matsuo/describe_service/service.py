from flask import request

from matsuo.service_base.service import HostedService
import boto3
import pprint
import json

from matsuo.utils.database.cache import DatabaseCache

bucket_name = 'uottahack18'
AWS_MAX_SIZE = 5 * 2 ** 20


class DescribeService(HostedService):
    SERVICE_NAME = 'Describe'

    def __init__(self, **kwargs):
        super().__init__(DescribeService.SERVICE_NAME, kwargs=kwargs)
        self.cache = DatabaseCache()
        self.client = boto3.client('rekognition', region_name='us-east-1')

    def start(self):
        self.host.add_endpoint('get_keywords', 'get_keywords', self.get_keywords, methods=['GET'])
        self.host.start()

    def get_keywords(self, *wargs, **kwargs):
        filename = request.args['image_id']
        data = self.cache.get_item(filename)
        if len(data) > AWS_MAX_SIZE:
            print("Image too big!")
            return json.dumps({'keywords': None})

        details = {'Bytes': data}
        if self.moderate(details):
            self.cache.remove_item(filename)
            return json.dumps({'keywords': None})

        return self._get_keywords(details)

    def _get_keywords(self, data):
        response = self.client.detect_labels(Image=data, MaxLabels=10, MinConfidence=60)
        keywords = [item['Name'] for item in response['Labels']]
        return json.dumps({'keywords': keywords})

    def moderate(self, data):
        moderation_labels = self.client.detect_moderation_labels(Image=data, MinConfidence=90)['ModerationLabels']
        if len(moderation_labels) > 0:
            print("Moderating Image")
            moderation_labels = set((label['Name'], label['ParentName'], label['Confidence'])
                                    for label in moderation_labels)
            pprint.pprint(moderation_labels)
            return True
        else:
            return False


class FileSizeLimitExceededError(LookupError):
    '''Files must be less that 5MB'''
