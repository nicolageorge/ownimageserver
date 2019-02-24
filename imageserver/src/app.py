import sys
import optparse
import os.path
import traceback

from flask import Flask
from flask import request
from flask import abort
from flask import render_template
# from flask import send_file

from lib.exceptions import BaseImageNotFound
from lib.exceptions import NotAnImageFile
from lib.image_provider import ImageProvider

import logging
FORMAT = '%(asctime)-15s %(message)s'
# logging.basicConfig(filename='app.log', level=logging.INFO, format=FORMAT)
logging.basicConfig(level=logging.INFO, format=FORMAT)

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    try:
        size = request.args.get('size', None);
        Provider = ImageProvider(path, size)
        return Provider.send_image()
    except BaseImageNotFound as e:
        abort(404)
        # return 'BaseImageNotFound: {}'.format(e.value)
    except NotAnImageFile as e:
        abort(404)
        # return 'I am an image server, {} is not a valid image size'.format(e.value)
    except Exception, e:
        return traceback.format_exc()
