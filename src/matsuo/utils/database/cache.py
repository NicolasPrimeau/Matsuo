from threading import Thread, Event

import datetime

import bson
import pymongo
from pymongo import MongoClient


class MemoryCache:

    def __init__(self):
        self.stop = Event()
        self.cleanup_task = CleanupTask(self.stop, self)
        self.cache = dict()

    def add_item(self, key, data):
        self.cache[key] = CacheItem(key, data)

    def get_item(self, key):
        if key not in self.cache:
            return None
        else:
            return self.cache[key].data

    def remove_item(self, key):
        if key in self.cache:
            self.cache.pop(key)

    def get_items(self):
        return list(self.cache.values())

    def terminate(self):
        self.stop.set()


class DatabaseCache:

    def __init__(self, database_name="Matsuo", collection_name="ImageCache",
                 expiration_time=datetime.timedelta(minutes=10)):
        self.client = MongoClient()[database_name][collection_name]
        self.expiration_delta = expiration_time
        if self.expiration_delta is not None:
            self.client.create_index([(DatabaseCacheItem.expiration_index, pymongo.ASCENDING)], expireAfterSeconds=0)
            self.client.create_index([(DatabaseCacheItem.expiration_index, pymongo.TEXT)])

    def add_item(self, key, data):
        item = DatabaseCacheItem(key, bson.binary.Binary(data.read()), datetime.datetime.now() + self.expiration_delta)
        self.client.update_one(item.get_id(), update=item.get_update_form(), upsert=True)

    def get_item(self, key):
        element = self.client.find_one({DatabaseCacheItem.filename_key: key})
        return element[DatabaseCacheItem.data_key] if element else None

    def remove_item(self, key):
        self.client.delete_many({DatabaseCacheItem.filename_key: key})


class DatabaseCacheItem:

    filename_key = 'filename'
    data_key = 'data'
    expiration_index = 'expireAt'

    def __init__(self, key, val, expiration_time):
        self.key = key
        self.val = val
        self.expiration = expiration_time

    def get_id(self):
        return {DatabaseCacheItem.data_key: self.key}

    def get_update_form(self):
        return {
            '$set': self.get_save_form()
        }

    def get_save_form(self):
        return {
            self.filename_key: self.key,
            self.data_key: self.val,
            self.expiration_index: self.expiration
        }


class CacheItem:

    def __init__(self, key, data, expiration_time_s=60*60):
        self.key = key
        self.data = data
        self.expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=expiration_time_s)

    def is_expired(self):
        return self.expiration_time < datetime.datetime.now()


class CleanupTask(Thread):

    def __init__(self, event, cache, period_s=60*5):
        super().__init__()
        self.stopped = event
        self.period_s = period_s
        self.cache = cache

    def start(self):
        while not self.stopped.wait(self.period_s):
            self._cleanup_cache()

    def _cleanup_cache(self):
        to_delete = [item for item in self.cache.get_items() if item.is_expired()]
        for item in to_delete:
            self.cache.remove_item(item.key)