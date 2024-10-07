from flask import Flask, request, send_file, render_template
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import logging
import os
import tempfile

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST"], allow_headers=["Content-Type"])

# Limit upload size to 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Ensure file is in request
        if 'image_file' not in request.files:
            return 'No file uploaded', 400

        image_file = request.files['image_file']

        # Use a temporary file to save the uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_input:
            image_file.save(temp_input.name)

            # Open the temporary image file
            try:
                input_image = Image.open(temp_input.name)
            except Exception as img_error:
                logging.error(f"Error opening image: {str(img_error)}")
                return 'Error in opening the image', 400

            # Check image size and convert to RGB if necessary
            if input_image.size[0] > 2000 or input_image.size[1] > 2000:  # Limit dimensions to 2000x2000 pixels
                return 'Image dimensions too large. Max 2000x2000 pixels.', 400

            # Ensure image is in a format suitable for processing
            if input_image.mode != 'RGB':
                input_image = input_image.convert('RGB')

            # Process the image using rembg
            output_image = remove(input_image)

            # Save the processed image to a byte stream
            img_io = io.BytesIO()
            output_image.save(img_io, 'PNG')
            img_io.seek(0)

        # Clean up the temporary file
        os.remove(temp_input.name)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        logging.error(f"Error processing the image: {str(e)}")
        return f"Error processing the image: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
