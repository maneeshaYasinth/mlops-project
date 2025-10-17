# predict.py

# Import the necessary parts from TensorFlow and other libraries
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

# --- 1. Load the Pre-trained Model ---
# We are loading MobileNetV2, which has been trained on the ImageNet dataset.
# This dataset contains over 1.4 million images across 1000 categories.
# The model weights are downloaded the first time you run this.
model = MobileNetV2(weights='imagenet')

def predict_image(img_path):
    """
    This function takes the path to an image, loads it, preprocesses it,
    and returns the top prediction from our model.
    """
    try:
        # --- 2. Load and Preprocess the Image ---
        # The model expects images to be exactly 224x224 pixels.
        img = image.load_img(img_path, target_size=(224, 224))
        
        # Convert the image to a format the model understands (a numpy array).
        img_array = image.img_to_array(img)
        
        # Add an extra dimension because the model expects a "batch" of images.
        img_array_expanded = np.expand_dims(img_array, axis=0)
        
        # Normalize the image data to be in the range the model was trained on.
        processed_img = preprocess_input(img_array_expanded)
        
        # --- 3. Make a Prediction ---
        predictions = model.predict(processed_img)
        
        # --- 4. Decode and Format the Result ---
        # The model returns a list of probabilities for all 1000 categories.
        # decode_predictions gives us the top predictions in a human-readable format.
        decoded_predictions = decode_predictions(predictions, top=1)[0]
        
        # Extract the top prediction's name and confidence
        top_prediction = decoded_predictions[0]
        name = top_prediction[1]
        confidence = top_prediction[2]
        
        return f"I'm {confidence:.2%} sure this is a {name.replace('_', ' ')}."

    except FileNotFoundError:
        return "Error: Image file not found."
    except Exception as e:
        return f"An error occurred: {e}"

# --- Main Execution Block ---
if __name__ == "__main__":
    # Define the path to your test image
    image_path = 'dog.webp' 
    
    # Get the prediction
    result = predict_image(image_path)
    
    # Print the result
    print(result)