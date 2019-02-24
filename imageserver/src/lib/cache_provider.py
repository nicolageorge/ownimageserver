import os
import mimetypes
from PIL import Image
import logging
log = logging.getLogger(__name__)

from flask import send_file

from exceptions import ImageNotInCache
from constants import IMAGE_CACHE_PATH

class FileCacheProvider(object):
    def __init__(self):
        pass

    def _build_path(self, name, width, height):
        name_chunks = name.split('.')
        full_path = '{0}/{1}_{2}x{3}{4}'.format(IMAGE_CACHE_PATH, name_chunks[0], width, height, name_chunks[1])
        return full_path

    def get_cached_image_path(self, name, width, height):
        thumb = self._build_path(name, width, height)
        if os.path.isfile(thumb):
            log.info('Image found in cache {}'.format(thumb))
            return thumb
        else:
            raise ImageNotInCache(thumb)

    def store(self, original, name, width, height):
        thumb = self._build_path(name, width, height)
        if os.path.isfile(thumb):
            return thumb
        else:
            try:
                im = Image.open(original)
                size = width, height
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(thumb, "JPEG")
                log.info('Image Stored in cache {}'.format(thumb))
                return thumb
            except IOError:
                log.error('IOError - cannot create thumbnail for {} on {}'.format(original, thumb))
                return ''
