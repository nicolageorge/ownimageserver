import os
import platform
import psutil

import redis

from constants import IMAGE_PATH
from constants import IMAGE_CACHE_PATH

import logging
log = logging.getLogger(__name__)


class StatisticsProvider(object):
    def __init__(self):
        self.data_cache = redis.Redis(host='redis', port=6379)

    def get_all_info(self):
        return {
            'images': {
                'cache_hits': int(self.data_cache.get('cache_hits')),
                'cache_misses': int(self.data_cache.get('cache_misses')),
                'cached_images_count': self._count_files(IMAGE_CACHE_PATH),
                'cached_location': IMAGE_CACHE_PATH,
                'images_count': self._count_files(IMAGE_PATH),
                'images_location': IMAGE_PATH,
            },
            'platform': {
                'boot_time': psutil.boot_time(),
                'os': platform.platform(),
            },
            'cpu': {
                'usage': psutil.cpu_percent(),
                'count': psutil.cpu_count(),
                'times': dict(psutil.cpu_times()._asdict()),
            },
            'memory': {
                'virtual': dict(psutil.virtual_memory()._asdict()),
                'swap': dict(psutil.swap_memory()._asdict()),
            }, 
            'disk': {
                'partitions': [dict(part._asdict()) for part in psutil.disk_partitions()],
                'usage': dict(psutil.disk_usage('/')._asdict()),
                'io_counters': dict(psutil.disk_io_counters(perdisk=False)._asdict()),
            },
        }

    def _count_files(self, absolute_path):
        files = []
        for name in os.listdir(absolute_path):
            path = '{}/{}'.format(absolute_path, name)
            if os.path.isfile(path):
                files.append(name) 
        count = len(files)
        del files
        return count
