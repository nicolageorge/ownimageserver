import os
import mimetypes
from PIL import Image
import logging
log = logging.getLogger(__name__)

from flask import send_file

from exceptions import ImageNotInCache

class FileCacheProvider(object):
    def __init__(self):
        pass

    def _build_path(self, location, name, width, height, extension):
        return '{0}/cache/{1}_{2}x{3}{4}'.format(location, name, width, height, extension)

    def send_image(self, location, name, extension, width, height):
        thumb = self._build_path(location, name, width, height, extension)
        if os.path.isfile(thumb):
            log.info('Image found in cache {}'.format(thumb))
            return send_file(thumb, mimetype=mimetypes.types_map[extension])
        else:
            raise ImageNotInCache(thumb)

    def store_image(self, original, location, name, extension, width, height):
        thumb = self._build_path(location, name, width, height, extension)
        if original != thumb:
            try:
                im = Image.open(original)
                size = width, height
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(thumb, "JPEG")
                log.info('Image Stored in cache {}'.format(thumb))
            except IOError:
                log.error('IOError - cannot create thumbnail for {}'.format(original))

    def store_and_send(self, original, location, name, extension, width, height):
        try:
            self.store_image(original, location, name, extension, width, height)
            return self.send_image(location, name, extension, width, height)
        except Exception:
            raise