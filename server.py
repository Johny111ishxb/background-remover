from flask import Flask, request, send_file, render_template
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST"], allow_headers=["Content-Type"])

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Check for file in request
        if 'image_file' not in request.files:
            return 'No file uploaded', 400

        image_file = request.files['image_file']

        # Check for valid file size (e.g., limit to 5MB)
        if image_file.content_length > 5 * 1024 * 1024:  # 5MB limit
            return 'File too large', 400

        try:
            input_image = Image.open(image_file.stream)
            # Optionally resize or process the image before passing to remove
            input_image.thumbnail((800, 800))  # Resize to a max of 800x800
        except Exception as img_error:
            logging.error(f"Error opening image: {str(img_error)}")
            return 'Error in opening the image', 400

        # Process the image using rembg
        output_image = remove(input_image)

        # Save the processed image to a byte stream
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        logging.error(f"Error processing the image: {str(e)}")
        return f"Error processing the image: {str(e)}", 500

# No need for if __name__ == '__main__': in production
