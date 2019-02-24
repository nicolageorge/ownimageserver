import os
import platform
import psutil

from constants import IMAGE_PATH
from constants import IMAGE_CACHE_PATH

import logging
log = logging.getLogger(__name__)



class StatisticsProvider(object):
    def __init__(self):
        self.image_count = None
        self.cache_count = None
        self.cache_hits = None
        self.cache_misses = None
        self.number_of_cached_images = None

    def get_all_info(self):
        return {
            'images': {
                'cached_images_count': self._count_files(IMAGE_CACHE_PATH),
                'image_count': self._count_files(IMAGE_PATH),
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
