@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image_file' not in request.files:
            return 'No file uploaded', 400

        image_file = request.files['image_file']
        input_image = Image.open(image_file.stream)

        # Reduce image size to lower memory consumption
        input_image.thumbnail((1024, 1024))  # Adjust the size as needed

        # Process the image
        output_image = remove(input_image)

        # Save the output image to a byte stream
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        print(f"Error processing the image: {str(e)}")
        return f"Error processing the image: {str(e)}", 500
