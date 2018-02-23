from threading import Thread, Event

import datetime


class Cache:

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