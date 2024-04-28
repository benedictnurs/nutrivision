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

def calculate_distance(p1, p2, ppi):
    """ Calculate the distance between two points based on PPI. """
    distance_pixels = np.linalg.norm(np.array(p1) - np.array(p2))
    return distance_pixels / ppi

def calculate_ppi(pixel_width_of_object, actual_width_in_inches):
    """ Calculate the pixels per inch (PPI) based on object width. """
    return pixel_width_of_object / actual_width_in_inches

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
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Process the image for hand landmarks
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.multi_hand_landmarks:
        return jsonify({'message': 'No hands detected'})

    # Manual input for reference object detection (to be replaced with actual detection logic)
    pixel_width_of_reference_object = 250  # Example pixel width of the object
    actual_width_of_reference_object = 3.5  # Example actual width in inches

    ppi = calculate_ppi(pixel_width_of_reference_object, actual_width_of_reference_object)

    for hand_landmarks in results.multi_hand_landmarks:
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

        height, width, _ = image.shape
        thumb_tip_pos = (int(thumb_tip.x * width), int(thumb_tip.y * height))
        index_tip_pos = (int(index_tip.x * width), int(index_tip.y * height))

        distance = calculate_distance(thumb_tip_pos, index_tip_pos, ppi)
        distance_text = f"{distance:.2f} inches"

        cv2.line(image, thumb_tip_pos, index_tip_pos, (255, 0, 0), 2)
        midpoint = ((thumb_tip_pos[0] + index_tip_pos[0]) // 2, (thumb_tip_pos[1] + index_tip_pos[1]) // 2)
        cv2.putText(image, distance_text, midpoint, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Convert image back to RGB for output
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
