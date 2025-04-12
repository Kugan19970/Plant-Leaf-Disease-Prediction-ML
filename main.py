from flask import Flask, render_template, request, jsonify
import numpy as np
import os
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
from googletrans import Translator
from disease_data import get_disease_details
from antibiotics import get_antibiotics_for_disease  # Import antibiotics function
from tutorial import *  # Import everything from tutorial Python file
from tutorial import get_video_url, get_seasonal_advice  # Import tutorial functions
from copy import deepcopy
from tts_service import tts_bp  # Import the Blueprint

# Initialize Flask app
app = Flask(__name__)

# Register Blueprint
app.register_blueprint(tts_bp, url_prefix="/")  # Ensure URL is correctly mapped


# Load the pre-trained model
model_filepath = 'model.h5'
model = load_model(model_filepath)
print("Model Loaded Successfully")

# Translator instance
translator = Translator()

# Function to predict tomato diseases
def predict_tomato_disease(image_path):
    test_image = load_img(image_path, target_size=(128, 128))  # Load image
    test_image = img_to_array(test_image) / 255  # Normalize
    test_image = np.expand_dims(test_image, axis=0)  # Model input shape

    result = model.predict(test_image)  # Predict the disease
    predicted_class = np.argmax(result, axis=1)[0]  # Get disease ID
    confidence = np.max(result) * 100  # Get the highest probability and convert to percentage

    # Get disease details from the external file
    return predicted_class, confidence, get_disease_details(predicted_class)



# Route for the home page
@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

# Route to fetch antibiotics for a given disease ID
@app.route('/antibiotics/<int:disease_id>')
def antibiotics(disease_id):
    lang = request.args.get("lang", "en")  # Default language is English
    antibiotics = get_antibiotics_for_disease(disease_id)

    if antibiotics:
        translated_antibiotics = deepcopy(antibiotics)  # Avoid modifying original data

        if lang == "ta":
            for antibiotic in translated_antibiotics:
                antibiotic["description"] = translator.translate(antibiotic["description"], dest="ta").text
                antibiotic["usage"] = translator.translate(antibiotic["usage"], dest="ta").text

        return render_template("antibiotics.html", antibiotics=translated_antibiotics, disease_id=disease_id, lang=lang)
    else:
        return render_template("error.html", message=f"No antibiotics found for Disease ID {disease_id}."), 404




# Route to handle prediction and display results
@app.route("/predict", methods=['POST'])
def predict():
    if 'image' not in request.files:
        return "No image uploaded!", 400

    file = request.files['image']
    if file.filename == '':
        return "No selected file!", 400

    # Save the uploaded file
    upload_folder = 'static/upload/'
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    # Predict the disease
    class_id, confidence, disease_info = predict_tomato_disease(file_path)

    # Print accuracy in Python console
    print(f"Disease ID: {class_id}, Confidence: {confidence:.2f}%")

    return render_template(
        'display.html',
        disease_id=class_id,
        disease_name=disease_info["name"],
        description=disease_info.get("description", "No description available."),
        solution=disease_info.get("solution", "No solution available."),
        recommendations=disease_info.get("recommendations", []),
        user_image=file.filename,
        confidence=confidence  # Pass accuracy percentage to the template
    )


# Route for tutorial videos and seasonal advice
@app.route('/tutorial', methods=['GET'])
def tutorial():
    disease_id = request.args.get('disease_id')
    season = request.args.get('season', 'summer')
    language = request.args.get('language', 'en')

    video_url = get_video_url(disease_id)
    seasonal_advice = get_seasonal_advice(season, language)

    return render_template('Tutorial.html', video_link=video_url, seasonal_advice=seasonal_advice)


@app.route("/translate_display", methods=["POST"])
def translate_display():
    try:
        data = request.json
        target_language = data.get("language", "en")
        disease_name = data.get("disease_name", "Disease Name: Late Blight")
        description = data.get("description", "A fungal disease affecting plants.")
        solution = data.get("solution", "Use copper-based fungicides.")
        recommendations = data.get("recommendations", ["Apply fungicide every 7 days."])

        # Translate all text fields
        translated_disease_name = translator.translate(disease_name, dest=target_language).text
        translated_description = translator.translate(description, dest=target_language).text  # Added description translation
        translated_solution = translator.translate(solution, dest=target_language).text
        translated_recommendations = [
            translator.translate(rec, dest=target_language).text for rec in recommendations
        ]

        # Debugging logs
        print("Translated Disease Name:", translated_disease_name)
        print("Translated Description:", translated_description)  # Added debugging log
        print("Translated Solution:", translated_solution)
        print("Translated Recommendations:", translated_recommendations)

        return jsonify({
            "disease_name": translated_disease_name,
            "description": translated_description,  # Added description in response
            "solution": translated_solution,
            "recommendations": translated_recommendations
        })

    except Exception as e:
        print("Error:", str(e))  # Print error message
        return jsonify({"error": str(e)}), 500  # Return HTTP 500 status for errors
    
# Run the app
if __name__ == "__main__":
    app.run(threaded=True, port=8080)
