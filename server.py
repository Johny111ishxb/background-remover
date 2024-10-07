from flask import Flask, request, send_file, render_template
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import logging
import psutil

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Enable CORS with methods and headers
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST"], allow_headers=["Content-Type"])

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file

def get_memory_usage():
    """Function to check current memory usage."""
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)  # in MB

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Ensure file is in request
        if 'image_file' not in request.files:
            return 'No file uploaded', 400

        image_file = request.files['image_file']
        logging.info(f"Uploaded image size: {image_file.content_length} bytes")

        # Load the image
        try:
            input_image = Image.open(image_file.stream)
            # Resize the image to limit memory usage
            max_size = (800, 800)  # Reduce max size to limit memory usage
            input_image.thumbnail(max_size, Image.ANTIALIAS)
            logging.info(f"Image loaded and resized: {input_image.size}")
        except Exception as img_error:
            logging.error(f"Error opening image: {str(img_error)}")
            return 'Error in opening the image', 400

        # Check memory usage before processing
        logging.info(f'Memory usage before processing: {get_memory_usage()} MB')

        # Process the image using rembg
        output_image = remove(input_image)

        # Check memory usage after processing
        logging.info(f'Memory usage after processing: {get_memory_usage()} MB')

        # Save the processed image to a byte stream
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        # Log and return a generic error message
        logging.error(f"Error processing the image: {str(e)}")
        return f"Error processing the image: {str(e)}", 500

# No need for if __name__ == '__main__': in production
from flask import Flask, request, send_file, render_template
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import logging
import psutil

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Enable CORS with methods and headers
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST"], allow_headers=["Content-Type"])

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file

def get_memory_usage():
    """Function to check current memory usage."""
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)  # in MB

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Ensure file is in request
        if 'image_file' not in request.files:
            return 'No file uploaded', 400

        image_file = request.files['image_file']
        logging.info(f"Uploaded image size: {image_file.content_length} bytes")

        # Load the image
        try:
            input_image = Image.open(image_file.stream)
            # Resize the image to limit memory usage
            max_size = (800, 800)  # Reduce max size to limit memory usage
            input_image.thumbnail(max_size, Image.ANTIALIAS)
            logging.info(f"Image loaded and resized: {input_image.size}")
        except Exception as img_error:
            logging.error(f"Error opening image: {str(img_error)}")
            return 'Error in opening the image', 400

        # Check memory usage before processing
        logging.info(f'Memory usage before processing: {get_memory_usage()} MB')

        # Process the image using rembg
        output_image = remove(input_image)

        # Check memory usage after processing
        logging.info(f'Memory usage after processing: {get_memory_usage()} MB')

        # Save the processed image to a byte stream
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        # Log and return a generic error message
        logging.error(f"Error processing the image: {str(e)}")
        return f"Error processing the image: {str(e)}", 500

# No need for if __name__ == '__main__': in production
