import os
import mimetypes

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
    def __init__(self, path, size):
        self.supported_formats = ['jpg', 'jpeg', 'png']
        self.path = path
        self.is_original = False
        if size is None:
            self.is_original = True
        else:
            try:
                [self.width, self.height] = [int(x) for x in size.split('x')]
            except:
                raise InvalidImageSize

        self.cache_provider = FileCacheProvider()

    def send_image(self):
        folder, name, full_path, extension = self.get_image_info(self.path)
        if not os.path.isfile(full_path):
            raise BaseImageNotFound(full_path)

        log.debug('ImageProvider.send_image {} {} {} {}'.format(folder, name, full_path, extension))
        if self.is_original:
            return send_file(full_path, mimetype=mimetypes.types_map[extension])

        try:
            return self.cache_provider.send_image(location=folder,
                                                  name=name,
                                                  extension=extension,
                                                  width=self.width,
                                                  height=self.height)
        except ImageNotInCache:
            log.info('ImageNotInCache {} {} {} {}'.format(folder, name, full_path, extension))
            return self.cache_provider.store_and_send(original=full_path,
                                                      location=folder,
                                                      name=name,
                                                      extension=extension,
                                                      width=self.width, 
                                                      height=self.height)

    def get_image_info(self, path):
        if len(path.split('/')) == 2:
            name = path.split('/')[1]
            name, extension = name.split('.')
            
            if extension not in self.supported_formats:
                raise NotAnImageFile

            extension = '.{}'.format(extension)
            full_path = '{}/{}{}'.format(IMAGE_PATH, name, extension)

            return IMAGE_PATH, name, full_path, extension
        else:
            raise NotAnImagePath
