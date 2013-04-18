import os
import logging
import re
import base64
import cStringIO
from PIL import Image
import numpy as np

from som.som_segmentation import *

from flask import Flask, jsonify, render_template
from flask.ext.restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
port = int(os.environ.get('PORT', 5000))

parser = reqparse.RequestParser()
parser.add_argument('img', type=str)


class ColorsExtractor(Resource):
    dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')

    def get(self):
        return 'Use PUT to send image'

    def post(self):
        args = parser.parse_args()
        logging.info('Received:' + str(args['img'][:35]))

        imgb64 = self.dataUrlPattern.match(args['img'])
        try:
            imgb64 = imgb64.group(2)
        except AttributeError:
            abort(404, message="Image format is wrong.")

        imgdata = None
        if imgb64 is not None and len(imgb64) > 0:
            imgdata = base64.b64decode(imgb64)

        tempimg = cStringIO.StringIO(imgdata)
        im = Image.open(tempimg)

        pixels = list(im.getdata())
        pixels = [(o[0]/255.0, o[1]/255.0, o[2]/255.0) for o in pixels]

        WR, WG, WB = som_train(pixels, 2)

        color_scores = som_score_colors(pixels, WR, WG, WB)
        logging.info('Scores:' + str(color_scores))

        d = {v: i for i, v in enumerate(color_scores)}
        color_scores.sort()

        # Add color 1
        idx = d[color_scores[-1]]
        results = [WR[0, idx],
                   WG[0, idx],
                   WB[0, idx]]
        # Add color 2
        idx = d[color_scores[-2]]
        results.extend([WR[0, idx],
                        WG[0, idx],
                        WB[0, idx]])
        results = map(lambda x: int(x * 255), results)

        logging.warning(('Colors:', results))

        return jsonify(colors=results)

api.add_resource(ColorsExtractor, '/colors')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
