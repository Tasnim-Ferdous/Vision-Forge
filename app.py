from flask import Flask, render_template, Response, request
import cv2
import numpy as np

app = Flask(__name__)

# Load overlay image with alpha channel
overlay_img = cv2.imread('static/overlays/sunglasses.png', cv2.IMREAD_UNCHANGED)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
camera = cv2.VideoCapture(0)

current_filter = "normal"
current_intensity = 5  # Default intensity

def overlay_transparent(background, overlay, x, y, scale=1):
    """Overlay transparent PNG on BGR background frame."""
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w = overlay.shape[:2]
    if x + w > background.shape[1] or y + h > background.shape[0]:
        return background  # Skip if overlay doesn't fit

    # Split overlay into channels
    if overlay.shape[2] < 4:
        return background  # No alpha channel, skip

    overlay_img = overlay[:, :, :3]
    mask = overlay[:, :, 3:] / 255.0

    roi = background[y:y+h, x:x+w]

    # Blend overlay on ROI
    blended = (1.0 - mask) * roi + mask * overlay_img
    background[y:y+h, x:x+w] = blended.astype(np.uint8)
    return background

def apply_filter(frame, filter_type, intensity):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if filter_type == "grayscale":
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif filter_type == "canny":
        threshold1 = max(10, min(100 * intensity // 10, 255))
        threshold2 = max(50, min(200 * intensity // 10, 255))
        edges = cv2.Canny(gray, threshold1, threshold2)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    elif filter_type == "invert":
        inv = cv2.bitwise_not(frame)
        alpha = max(0.0, min(intensity / 10.0, 1.0))
        return cv2.addWeighted(inv, alpha, frame, 1 - alpha, 0)
    elif filter_type == "blur":
        k = max(1, min(intensity * 2 + 1, 31))
        return cv2.GaussianBlur(frame, (k, k), 0)
    elif filter_type == "face":
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return frame
    elif filter_type == "thermal":
        normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        colored = cv2.applyColorMap(normalized, cv2.COLORMAP_JET)
        alpha = max(0.1, min(intensity / 10.0, 1.0))
        blended = cv2.addWeighted(colored, alpha, frame, 1 - alpha, 0)
        return blended
    elif filter_type == "face_overlay":
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in faces:
            scale = w / overlay_img.shape[1] * 1.1
            y_offset = int(y + h * 0.25)
            frame = overlay_transparent(frame, overlay_img, x, y_offset, scale)
        return frame

    return frame

def generate_frames(split_view=False):
    global current_filter, current_intensity
    while True:
        success, frame = camera.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)

        if split_view:
            filtered = apply_filter(frame.copy(), current_filter, current_intensity)
            height, width = frame.shape[:2]
            target_width = 320
            target_height = int(target_width * height / width)

            orig_resized = cv2.resize(frame, (target_width, target_height))
            filtered_resized = cv2.resize(filtered, (target_width, target_height))

            if width >= height:  # Landscape: side-by-side
                combined = cv2.hconcat([orig_resized, filtered_resized])
            else:  # Portrait: top-bottom
                combined = cv2.vconcat([orig_resized, filtered_resized])
        else:
            combined = apply_filter(frame, current_filter, current_intensity)

        ret, buffer = cv2.imencode('.jpg', combined)
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(split_view=False),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_split')
def video_feed_split():
    return Response(generate_frames(split_view=True),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/frame')
def frame_route():
    global current_filter, current_intensity
    current_filter = request.args.get("effect", "normal")
    intensity = request.args.get("intensity")
    if intensity and intensity.isdigit():
        current_intensity = int(intensity)
    else:
        current_intensity = 5
    return "", 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
