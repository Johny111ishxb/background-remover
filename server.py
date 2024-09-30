from flask import Flask, request, send_file, render_template  # Import render_template
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import os  # Import os module

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file

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
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)  # Update for deployment
