import os
import unittest

from app.lib.image_provider import ImageProvider
from app.lib.constants import IMAGE_PATH
from mock import MagicMock

class TestImageProvider(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_send_image(self):
    	provider = ImageProvider('imag6.jpg', '500x500')
    	provider._send_file = MagicMock(return_value='sending image..')
    	self.assertEquals(provider.send_image(), 'sending image..')

    def test_get_image_info(self):
        provider = ImageProvider('imag6.jpg', '500x500')
        test_path, test_ext = provider._get_image_info()
        good_path = '{}/{}'.format(IMAGE_PATH, 'imag6.jpg')
        good_extension = '.jpg'
        self.assertEquals(test_path, good_path)
        self.assertEquals(test_ext, good_extension)

    def test_class_constructor(self):
        provider = ImageProvider('imag6.jpg', '400x500')
        self.assertEquals(provider.width, 400)
        self.assertEquals(provider.height, 500)
        self.assertEquals(provider.is_original, False)

        second_provider = ImageProvider('imag6.jpg', None)
        self.assertEquals(second_provider.width, None)
        self.assertEquals(second_provider.width, None)
        self.assertEquals(second_provider.is_original, True)


if __name__ == '__main__':
    unittest.main()