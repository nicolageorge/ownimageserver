import os
import unittest
import requests
import json

# IMAGE_PATH = os.environ.get('OWNZONES_IMAGE_PATH')


class TestServer(unittest.TestCase):
    def setUp(self):
        self.images = ['imag6.jpg', 'imag11.jpg', 'imag2.jpg', 'imag10.jpg',
                       'imag3.jpeg', 'imag12.jpg', 'imag8.jpg', 'imag7.jpg',
                       'imag5.jpg', 'imag1.jpg', 'imag9.jpg', 'imag3.jpg', 'imag4.jpg']

    def tearDown(self):
        del self.images

    def _do_image_request(self, image, width=None, height=None):
        if width and height:
            url = 'http://imageserver:8000/images/{}?size={}x{}'.format(image, width, height)
        else:
            url = 'http://imageserver:8000/images/{}'.format(image)
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

    def test_statistics(self):
        url = 'http://imageserver:8000/statistics'
        r = requests.get(url)
        self.assertEqual(r.status_code, 200, 'Should be 200')
        self.assertEqual(r.headers['content-type'], 'application/json', 'Should be application json')

        statistics = json.loads(r.text)
        self.assertTrue('cpu' in statistics)
        self.assertTrue('disk' in statistics)
        self.assertTrue('images' in statistics)
        self.assertTrue('memory' in statistics)
        self.assertTrue('platform' in statistics)


if __name__ == '__main__':
    unittest.main()
