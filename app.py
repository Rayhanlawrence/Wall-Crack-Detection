from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB max upload size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Load the CNN model once when the app starts
<<<<<<< HEAD
model = load_model('model/model_retak_dinding_balanced.h5')
=======
model = load_model('model/crack_detection_model.h5')
>>>>>>> 762aff706cbc30bb8b9b5f512c4e50cc7af63cba

# Print model input shape for debugging
print("Model input shape:", model.input_shape)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(img_path):
    # Gunakan load_img seperti di notebook!
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# def preprocess_image(img_path):
#     img = Image.open(img_path).convert('RGB')
#     # Resize image to model's expected input size dynamically
#     input_shape = model.input_shape  # e.g. (None, height, width, channels)
#     if len(input_shape) == 4:
#         _, height, width, channels = input_shape
#     else:
#         # fallback default size
#         height, width = 150, 150
    

#     img = img.resize((width, height))
#     # print("Model expects input shape:", model.input_shape)
#     assert img.size == (150, 150), "Ukuran gambar tidak sesuai dengan input model!"
#     print("Ukuran gambar:", img.size)
#     img_array = image.img_to_array(img)
#     img_array = img_array / 255.0  # Normalize to [0,1]
#     img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
#     return img_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uji-gambar', methods=['GET', 'POST'])
def uji_gambar():
    result = None
    filename = None
    confidence = None
    raw_prediction = None
    if request.method == 'POST':
        if 'image' not in request.files:
            result = "Tidak ada file yang diupload."
        else:
            file = request.files['image']
            if file.filename == '':
                result = "Tidak ada file yang dipilih."
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Preprocess image and predict
                img_array = preprocess_image(filepath)
                prediction = model.predict(img_array)[0][0]
                raw_prediction = prediction
                confidence = float(prediction) * 100

                threshold = 0.5  # Threshold for crack detection
                print(prediction)
                if prediction > threshold:
<<<<<<< HEAD
                    result = "⚠️ Retak Terdeteksi"
                else:
                    result = "✅ Tidak Ada Retak"
=======
                    result = "✅ Tidak Ada Retak"
                else:
                    result = "⚠️ Retak Terdeteksi"
>>>>>>> 762aff706cbc30bb8b9b5f512c4e50cc7af63cba
            else:
                result = "Format file tidak didukung. Gunakan .jpg, .jpeg, atau .png."
    return render_template('uji_gambar.html', result=result, filename=filename, confidence=confidence, raw_prediction=raw_prediction)

@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

@app.route('/kontak')
def kontak():
    return render_template('kontak.html')

@app.route('/hasil-contoh')
def hasil_contoh():
    return render_template('hasil_contoh.html')

if __name__ == '__main__':
    app.run(debug=True)
