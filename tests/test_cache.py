import os
import unittest

from app.lib.cache_provider import FileCacheProvider
from app.lib.constants import IMAGE_PATH
from app.lib.constants import IMAGE_CACHE_PATH

class TestCache(unittest.TestCase):
    def test_build_path(self):
        cache = FileCacheProvider()
        cache_path = cache._build_path('imag6.jpg', 640, 480)
        good_path = '{}/imag6_640x480.jpg'.format(IMAGE_CACHE_PATH)
        self.assertEquals(cache_path, good_path)

    def test_store(self):
    	cache = FileCacheProvider()
    	original_path = '{}/imag5.jpg'.format(IMAGE_PATH)
    	cached_image = cache.store(original_path, 'imag5.jpg', 640, 480)
    	self.assertTrue(os.path.isfile(cached_image))


if __name__ == '__main__':
    unittest.main()