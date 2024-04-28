from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np
import mediapipe as mp
from PIL import Image
from io import BytesIO

app = Flask(__name__)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

def calculate_distance(p1, p2, ppi=72):
    # Assuming screen ppi (pixels per inch) is 72 by default; adjust as needed
    distance_pixels = np.linalg.norm(np.array(p1) - np.array(p2))
    return distance_pixels / ppi

@app.route('/api', methods=['POST'])
def upload_image():
    data = request.json
    if not data or 'image' not in data:
        return jsonify({'message': 'No image provided'}), 400

    # Decode the image data
    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    image = np.array(image)

    # Convert RGB to BGR for OpenCV processing
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Process the image for hand landmarks
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.multi_hand_landmarks:
        return jsonify({'message': 'No hands detected'})

    for hand_landmarks in results.multi_hand_landmarks:
        # Get fingertip positions
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # Convert normalized positions to pixel values
        height, width, _ = image.shape
        thumb_tip_pos = (int(thumb_tip.x * width), int(thumb_tip.y * height))
        index_tip_pos = (int(index_tip.x * width), int(index_tip.y * height))

        # Draw line between thumb tip and index finger tip
        cv2.line(image, thumb_tip_pos, index_tip_pos, (255, 0, 0), 5)

        # Calculate distance in inches
        distance = calculate_distance(thumb_tip_pos, index_tip_pos)

        # Convert image back to RGB for PIL compatibility
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(image)
        buffered = BytesIO()
        img_pil.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return jsonify({
            'message': 'Distance calculated',
            'distance_inches': distance,
            'image_with_line': img_str
        })

if __name__ == '__main__':
    app.run(debug=True)
