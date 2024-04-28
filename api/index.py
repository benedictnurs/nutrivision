from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
import numpy as np

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    image_data = data['image']
    # Remove the header from the base64 string and decode
    header, encoded = image_data.split(",", 1)
    image_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_bytes))
    
    # Process the image or save it
    image.save('received_image.png')  # Example: Saving the image

    return jsonify({'message': 'Image received successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
