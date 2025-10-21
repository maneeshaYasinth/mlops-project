# app.py

import os
from flask import Flask, request, jsonify

# Import the prediction function from your predict.py file
from predict import predict_image

# Create a Flask web server
app = Flask(__name__)

# Define the upload folder and allowed file types
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# A simple function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create the /predict route
@app.route('/predict', methods=['POST'])
def upload_and_predict():
    # 1. Check if a file was sent in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    # 2. Check if the file is valid
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    
    if file and allowed_file(file.filename):
        # 3. Save the file temporarily
        # Ensure the 'uploads' directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) 
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        try:
            # 4. Get the prediction
            prediction_result = predict_image(filepath)
            
            # 5. Clean up the uploaded file
            os.remove(filepath) 
            
            # 6. Send the result back as JSON
            return jsonify({'prediction': prediction_result})
        
        except Exception as e:
            # Clean up even if an error occurs
            os.remove(filepath)
            return jsonify({'error': f'Error during prediction: {e}'}), 500
    
    else:
        return jsonify({'error': 'File type not allowed'}), 400

# This runs the web server
if __name__ == '__main__':
    # 'host=0.0.0.0' makes it accessible on your local network
    app.run(host='0.0.0.0', port=5000)