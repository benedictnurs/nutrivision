from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np
import mediapipe as mp
from PIL import Image
from io import BytesIO
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

def calculate_distance(p1, p2, ppi):
    """ Calculate the distance between two points based on PPI. """
    distance_pixels = np.linalg.norm(np.array(p1) - np.array(p2))
    return distance_pixels / ppi

def calculate_ppi(pixel_width_of_object, actual_width_in_inches):
    """ Calculate the pixels per inch (PPI) based on object width. """
    return pixel_width_of_object / actual_width_in_inches

@app.route('/api', methods=['POST'])
def upload_image():
    app.logger.debug("Request received with data: %s", request.data)
    data = request.json
    if not data or 'image' not in data:
        return jsonify({'message': 'No image provided'}), 400

    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.multi_hand_landmarks:
        return jsonify({'message': 'No hands detected'})

    finger_tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]

    height, width, _ = image.shape
    distances = {}

    # Calculate distances between each pair of fingertips
    for i, tip1 in enumerate(finger_tips):
        for j, tip2 in enumerate(finger_tips[i+1:], i+1):
            pos1 = (int(results.multi_hand_landmarks[0].landmark[tip1].x * width),
                    int(results.multi_hand_landmarks[0].landmark[tip1].y * height))
            pos2 = (int(results.multi_hand_landmarks[0].landmark[tip2].x * width),
                    int(results.multi_hand_landmarks[0].landmark[tip2].y * height))
            distance = calculate_distance(pos1, pos2, 300)  # Example PPI, replace with dynamic calculation
            distances[f"{tip1}-{tip2}"] = f"{distance:.2f} inches"
            cv2.line(image, pos1, pos2, (255, 0, 0), 2)

    # Convert image back to RGB for output
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(image)
    buffered = BytesIO()
    img_pil.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return jsonify({
        'message': 'Distance calculated',
        'distances': distances,
        'image_with_line': img_str
    })

if __name__ == '__main__':
    app.run(debug=True)
