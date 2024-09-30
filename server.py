from flask import Flask, request, send_file, render_template
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST"], allow_headers=["Content-Type"])  # Enable CORS with methods and headers

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image_file' not in request.files:
            return 'No file uploaded', 400

        image_file = request.files['image_file']
        input_image = Image.open(image_file.stream)

        # Ensure the image is opened correctly
        if input_image is None:
            return 'Error in opening the image', 400

        # Process the image
        output_image = remove(input_image)

        # Save the output image to a byte stream
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        # Log the error and return a generic error message
        print(f"Error processing the image: {str(e)}")
        return f"Error processing the image: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)  # Run with debug mode enabled
