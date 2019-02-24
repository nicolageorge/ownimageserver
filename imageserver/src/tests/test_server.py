import os
import unittest
import requests

IMAGE_PATH = os.environ.get('OWNZONES_IMAGE_PATH')

class TestServer(unittest.TestCase):
    def setUp(self):
        self.images = []
        for name in os.listdir(IMAGE_PATH):
            path = '{}/{}'.format(IMAGE_PATH, name)
            if os.path.isfile(path):
                self.images.append(name)


    def tearDown(self):
        del self.images

    def _do_image_request(self, image, width=None, height=None):
        if width and height:
            url = 'http://0.0.0.0:8000/images/{}?size={}x{}'.format(image, width, height)
        else:
            url = 'http://0.0.0.0:8000/images/{}'.format(image)
        return requests.get(url)

    def test_for_200_response(self):
        r = self._do_image_request(self.images[0])
        self.assertEqual(r.status_code, 200, 'Should be 200')

    def test_for_404_response(self):
        r = self._do_image_request('thisshouldneverbeanimagenamethatiswhyiammakingitthislong.jpg')
        self.assertEqual(r.status_code, 404, 'Should be 404')        

    def test_all_images(self):
        for image in self.images:
            r = self._do_image_request(image)
            self.assertEqual(r.status_code, 200, 'Should be 200')

    def test_cache_generation(self):
        for height in xrange(300, 310):
            for width in xrange(400, 405):
                for image in self.images[::2]:
                    r = self._do_image_request(image, width=width, height=height)
                    self.assertEqual(r.status_code, 200, 'Should be 200')


if __name__ == '__main__':
    unittest.main()