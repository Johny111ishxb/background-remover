from flask import Flask, request, send_file, render_template
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

# Enable CORS for all routes and methods
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST"], allow_headers=["Content-Type"])

@app.route('/')
def home():
    # Serve the homepage
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image_file' not in request.files:
            return 'No file uploaded', 400
        
        # Get the uploaded image
        image_file = request.files['image_file']
        input_image = Image.open(image_file.stream)

        # Reduce the image size to lower memory usage (Optional: Adjust the size as needed)
        input_image.thumbnail((1024, 1024))  # This limits the size without affecting aspect ratio
        
        # Remove background using rembg
        output_image = remove(input_image)

        # Save the processed image to a byte stream
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)

        # Return the processed image as a PNG
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        # Print the error for debugging and return a generic message to the user
        print(f"Error processing the image: {str(e)}")
        return f"Error processing the image: {str(e)}", 500

if __name__ == '__main__':
    # Don't include app.run() for production when using Gunicorn or another WSGI server
    pass
