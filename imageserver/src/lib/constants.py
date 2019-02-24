from os import environ

APP_PATH = '/srv/ownzones/imageserver'
IMAGE_PATH = environ.get('OWNZONES_IMAGE_PATH')
IMAGE_CACHE_PATH = environ.get('OWNZONES_IMAGE_CACHE_PATH')