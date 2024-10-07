from flask import Flask, request, send_file, render_template
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Enable CORS with methods and headers
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST"], allow_headers=["Content-Type"])

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if the file is in the request
    if 'image_file' not in request.files:
        logging.error("No file uploaded")
        return 'No file uploaded', 400

    image_file = request.files['image_file']

    try:
        # Attempt to open the uploaded image
        input_image = Image.open(image_file.stream)
    except Exception as img_error:
        logging.error(f"Error opening image: {str(img_error)}")
        return 'Error in opening the image', 400

    try:
        # Process the image using rembg
        output_image = remove(input_image)

        # Save the processed image to a byte stream
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)

        # Return the processed image as a response
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        logging.error(f"Error processing the image: {str(e)}")
        return 'Error processing the image', 500

# This is the entry point when running the app
if __name__ == '__main__':
    app.run(debug=True)  # Set debug=True for development; set to False in production
