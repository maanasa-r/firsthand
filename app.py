import os
import cv2
from flask import Flask, render_template, Response, request, jsonify
from inference import get_model
from google import genai

app = Flask(__name__)

# Initialize Roboflow model
try:
    api_key = os.environ.get("ROBOFLOW_API_KEY")
    if api_key:
        model = get_model(model_id="asl-american-sign-language/1", api_key=api_key)
    else:
        print("ROBOFLOW_API_KEY not set. Using without explicit key (might fail).")
        model = get_model(model_id="asl-american-sign-language/1")
except Exception as e:
    print(f"Error loading Roboflow model: {e}")
    model = None

# Initialize Gemini Client
genai_client = None
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai_client = genai.Client(api_key=api_key)
    else:
        print("GEMINI_API_KEY not set. Coaching will not work.")
except Exception as e:
    print(f"Error initializing Gemini: {e}")

# Global variables to track the current detection state
current_detection = None

def generate_frames():
    global current_detection
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        print("Error: Could not open video device.")
        return

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            if model:
                # Run Roboflow inference
                results = model.infer(frame)
                annotated_frame = frame.copy()
                
                predictions = []
                # Handle different formats returned by inference package
                if isinstance(results, list) and len(results) > 0:
                    predictions = getattr(results[0], 'predictions', [])
                elif hasattr(results, 'predictions'):
                    predictions = results.predictions

                if len(predictions) > 0:
                    largest_area = 0
                    best_pred = None
                    
                    for pred in predictions:
                        # pred could be a dict or object
                        width = pred.width if hasattr(pred, 'width') else pred.get('width', 0)
                        height = pred.height if hasattr(pred, 'height') else pred.get('height', 0)
                        area = width * height
                        if area > largest_area:
                            largest_area = area
                            best_pred = pred
                            
                    conf = best_pred.confidence if hasattr(best_pred, 'confidence') else best_pred.get('confidence', 0)
                    if best_pred and conf > 0.3:
                        class_name = best_pred.class_name if hasattr(best_pred, 'class_name') else best_pred.get('class', '')
                        current_detection = class_name
                        
                        # Draw bounding box for ONLY the largest instance
                        x = best_pred.x if hasattr(best_pred, 'x') else best_pred.get('x', 0)
                        y = best_pred.y if hasattr(best_pred, 'y') else best_pred.get('y', 0)
                        width = best_pred.width if hasattr(best_pred, 'width') else best_pred.get('width', 0)
                        height = best_pred.height if hasattr(best_pred, 'height') else best_pred.get('height', 0)
                        
                        xmin = int(x - width / 2)
                        ymin = int(y - height / 2)
                        xmax = int(x + width / 2)
                        ymax = int(y + height / 2)
                        
                        cv2.rectangle(annotated_frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                        cv2.putText(annotated_frame, f"{class_name} {conf:.2f}", 
                                   (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    else:
                        current_detection = None
                else:
                    current_detection = None
            else:
                annotated_frame = frame

            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
    camera.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/current_state', methods=['GET'])
def get_current_state():
    return jsonify({"detection": current_detection})

@app.route('/api/get_coaching', methods=['POST'])
def get_coaching():
    data = request.json
    target = data.get('target')
    detected = data.get('detected')
    
    if not target:
        return jsonify({"error": "Target not provided"}), 400
        
    if not genai_client:
        return jsonify({"error": "Gemini API key not configured"}), 500

    prompt = (
        f"The user is trying to sign the ASL letter/word '{target}'. "
        f"However, they are currently signing something that looks like '{detected}'. "
        f"Please provide a brief, friendly, constructive coaching tip on how they should shape their fingers "
        f"or change palm orientation to correctly sign '{target}'. Keep it to 1-2 short sentences."
    )

    try:
        response = genai_client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
        )
        return jsonify({"coaching": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
