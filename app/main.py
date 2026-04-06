from flask import Flask, request, jsonify, render_template
from app.model import predict
from app.rules import get_disposal_guidance

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Use PNG, JPG, or WEBP.'}), 400
    image_bytes = file.read()
    predicted_class, confidence = predict(image_bytes)
    guidance = get_disposal_guidance(predicted_class, confidence)
    return jsonify(guidance)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)