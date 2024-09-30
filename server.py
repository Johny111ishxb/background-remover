import os
import logging
from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)  # Add this line to enable logging

@app.route('/upload', methods=['POST'])
def upload_image():
    logging.debug('Upload route triggered')
    if 'image_file' not in request.files:
        logging.error('No file uploaded')
        return 'No file uploaded', 400

    try:
        image_file = request.files['image_file']
        input_image = Image.open(image_file.stream)
        logging.debug('Image uploaded successfully')
        output_image = remove(input_image)

        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        logging.error(f'Error processing image: {e}')
        return 'Internal server error', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
