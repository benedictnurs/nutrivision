from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np
import mediapipe as mp
from PIL import Image
from io import BytesIO

app = Flask(__name__)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

def detect_gesture(landmarks, image_width, image_height):
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]

    # Simple gesture recognition logic
    if thumb_tip.y < index_finger_tip.y < middle_finger_tip.y < ring_finger_tip.y < pinky_tip.y:
        return "Thumbs Up"
    elif thumb_tip.x < index_finger_tip.x and index_finger_tip.y < middle_finger_tip.y:
        return "Victory"
    # Count fingers shown
    fingers = [thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip]
    count_fingers = sum(1 for finger in fingers if finger.y < ring_finger_tip.y - 0.1)
    return f"{count_fingers} fingers shown"

def label_image(image, gesture, location):
    cv2.putText(image, gesture, (int(location.x * image.shape[1]), int(location.y * image.shape[0])),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

@app.route('/api', methods=['POST'])
def upload_image():
    data = request.json
    if not data or 'image' not in data:
        return jsonify({'message': 'No image provided'}), 400

    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    image = np.array(image)
    if image.ndim == 2:  # Convert grayscale to RGB
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    results = hands.process(image)
    if not results.multi_hand_landmarks:
        return jsonify({'message': 'No hands detected'})

    gestures = []
    image_height, image_width, _ = image.shape
    for hand_landmarks in results.multi_hand_landmarks:
        gesture = detect_gesture(hand_landmarks.landmark, image_width, image_height)
        gestures.append(gesture)
        mp.solutions.drawing_utils.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
            mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
            mp.solutions.drawing_styles.get_default_hand_connections_style())
        # Label the gesture on the image
        label_image(image, gesture, hand_landmarks.landmark[mp_hands.HandLandmark.WRIST])

    # Ensure image is in RGB for output
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(image)
    buffered = BytesIO()
    img_pil.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return jsonify({
        'message': 'Hand and finger tracking complete with gestures labeled',
        'image_with_tracking': img_str,
        'gestures': gestures
    })

if __name__ == '__main__':
    app.run(debug=True)
