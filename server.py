from rembg import remove
from PIL import Image
import io

# Cache the model
model = None

def get_model():
    global model
    if model is None:
        model = remove  # Initialize the model only once
    return model

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image_file' not in request.files:
            return 'No file uploaded', 400

        image_file = request.files['image_file']
        input_image = Image.open(image_file.stream)

        # Resize image to reduce memory usage
        input_image.thumbnail((800, 800))  # Resize the image

        # Perform background removal using the cached model
        output_image = get_model()(input_image)

        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        print(f"Error processing image: {e}")
        return f"Error: {e}", 500
