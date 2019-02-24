import sys
import optparse
import os.path
import traceback

from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
# from flask import send_file

from lib.exceptions import BaseImageNotFound
from lib.exceptions import NotAnImageFile
from lib.image_provider import ImageProvider
from lib.statistics_provider import StatisticsProvider

import logging
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    chunks = path.split('/')
    if chunks[0] == 'images':
        try:
            size = request.args.get('size', None);
            image_provider = ImageProvider(chunks[1], size)
            return image_provider.send_image()
        except BaseImageNotFound as e:
            abort(404)
            # return 'BaseImageNotFound: {}'.format(e.value)
        except NotAnImageFile as e:
            abort(404)
            # return 'I am an image server, {} is not a valid image size'.format(e.value)
        except Exception, e:
            return traceback.format_exc()
    elif chunks[0] =='statistics':
        stats_provider = StatisticsProvider()
        stats = stats_provider.get_all_info()
        return jsonify(stats)
    else:
        return 'Unknown Service'