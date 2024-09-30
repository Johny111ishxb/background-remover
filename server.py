from flask import Flask, request, send_file
from flask_cors import CORS  # Import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image_file' not in request.files:
        return 'No file uploaded', 400

    image_file = request.files['image_file']
    input_image = Image.open(image_file.stream)
    output_image = remove(input_image)

    img_io = io.BytesIO()
    output_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
