import os
import mimetypes

import redis
from flask import send_file

from cache_provider import FileCacheProvider

from constants import IMAGE_PATH

from exceptions import NotAnImagePath
from exceptions import InvalidImageSize
from exceptions import ImageNotInCache
from exceptions import NotAnImageFile
from exceptions import BaseImageNotFound

import logging
log = logging.getLogger(__name__)

class ImageProvider(object):
    def __init__(self, name, size):
        self.supported_formats = ['jpg', 'jpeg', 'png']
        self.name = name
        self.is_original = False
        self.width, self.height = None, None
        if size is None:
            self.is_original = True
        else:
            try:
                [self.width, self.height] = [int(x) for x in size.split('x')]
            except:
                raise InvalidImageSize

        self.object_cache = FileCacheProvider()
        self.data_cache = redis.Redis(host='redis', port=6379)


    def increase_data_cache(self, redis_key):
        try:
            return self.data_cache.incr(redis_key)
        except redis.exceptions.ConnectionError as exc:
            log.error('cache hits could not be increased')

    def _send_file(self, full_path, ext):
        return send_file(full_path, mimetype=mimetypes.types_map[ext])

    def send_image(self):
        full_path, ext = self._get_image_info()
        
        log.debug('ImageProvider.send_image path: {},name : {}, ext: {}, size: {}x{}'\
                   .format(full_path, self.name, ext, self.width, self.height))

        if not os.path.isfile(full_path):
            raise BaseImageNotFound(full_path)

        if self.is_original:
            self.increase_data_cache('original_hits')
            return self._send_file(full_path, ext)

        try:
            path = self.object_cache.get_cached_image_path(name=self.name, width=self.width, height=self.height)
            self.increase_data_cache('cache_hits')
            return self._send_file(path, ext)
        except ImageNotInCache as e:
            log.info('ImageProvider.ImageNotInCache path: {},name : {}, ext: {}, size: {}x{}'\
                      .format(full_path, self.name, ext, self.width, self.height))
            self.increase_data_cache('cache_misses')
            cached_image_path = self.object_cache.store(original=full_path,
                                                 name=self.name,
                                                 width=self.width,
                                                 height=self.height)
            if os.path.isfile(cached_image_path):
                return self._send_file(cached_image_path, ext)
            else:
                raise IOError

    def _get_image_info(self):
        extension = '.{}'.format(self.name.split('.')[1])
        full_path = '{}/{}'.format(IMAGE_PATH, self.name)
        return full_path, extension