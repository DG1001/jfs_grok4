import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory, abort
import threading
import time

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MAX_IMAGES = 10
VISIBLE_TIME = 5  # seconds
FADE_TIME = 10
TOTAL_TIME = VISIBLE_TIME + FADE_TIME
DATA_FILE = 'data.json'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_images():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)['images']
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_images(images):
    with open(DATA_FILE, 'w') as f:
        json.dump({'images': images}, f)

def cleanup_thread():
    while True:
        now = datetime.now()
        images = load_images()
        new_images = []
        for img in images:
            ts = datetime.fromisoformat(img['timestamp'])
            age = (now - ts).total_seconds()
            if age < TOTAL_TIME:
                new_images.append(img)
            else:
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, img['filename']))
                except OSError:
                    pass
        if len(new_images) != len(images):
            save_images(new_images)
        time.sleep(1)

threading.Thread(target=cleanup_thread, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    comment = request.form.get('comment', '')
    if not file or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if len(comment) > 100:
        return jsonify({'error': 'Comment too long'}), 400
    if file.content_length > 5 * 1024 * 1024:
        return jsonify({'error': 'File too large'}), 400
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ('.jpg', '.jpeg', '.png', '.webp'):
        return jsonify({'error': 'Invalid file type'}), 400
    # Generate unique filename
    timestamp = datetime.now().isoformat().replace(':', '').replace('-', '').replace('.', '')
    filename = f"{timestamp}{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    images = load_images()
    new_img = {
        'filename': filename,
        'comment': comment,
        'timestamp': datetime.now().isoformat()
    }
    images.append(new_img)
    if len(images) > MAX_IMAGES:
        oldest = images.pop(0)
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, oldest['filename']))
        except OSError:
            pass
    save_images(images)
    return jsonify({'success': True}), 200

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/api/images')
def api_images():
    images = load_images()
    now = datetime.now()
    current_images = []
    for img in images:
        ts = datetime.fromisoformat(img['timestamp'])
        age = (now - ts).total_seconds()
        if age < TOTAL_TIME:
            status = 'visible' if age < VISIBLE_TIME else 'fading'
            current_images.append({
                'filename': img['filename'],
                'comment': img['comment'],
                'age': age,
                'status': status
            })
    return jsonify(current_images)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except:
        abort(404)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
