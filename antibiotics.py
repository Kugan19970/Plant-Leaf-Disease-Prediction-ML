from flask import Flask, render_template, request, url_for
from googletrans import Translator
from copy import deepcopy

app = Flask(__name__)
translator = Translator()  # ✅ Create a translator instance

# Antibiotic details
antibiotic_data = {
    "A1": {
        "name": "Streptomycin Sulfate",
        "description": "Effective for bacterial diseases like bacterial spot and bacterial speck.",
        "usage": "Apply as a foliar spray at intervals of 7–10 days."
    },
    "A2": {
        "name": "Kasugamycin",
        "description": "Effective against bacterial spot and canker, reduces pathogen resistance risks.",
        "usage": "Use as a foliar spray; apply during active bacterial infection."
    },
    "A3": {
        "name": "Copper Hydroxide",
        "description": "Broad-spectrum control against bacterial and fungal diseases.",
        "usage": "Apply as a preventive spray; effective for bacterial diseases and late blight."
    },
    "A4": {
        "name": "Oxytetracycline",
        "description": "Targets bacterial diseases like bacterial wilt and bacterial spot.",
        "usage": "Apply as a foliar spray or soil drench; consult guidelines for use."
    },
    "A5": {
        "name": "Hydrogen Peroxide and Peracetic Acid Mix",
        "description": "A sanitizing treatment for bacterial and fungal pathogens.",
        "usage": "Use as a foliar spray or for sterilizing equipment."
    },
    "A6": {
        "name": "Azoxystrobin",
        "description": "Highly effective against fungal diseases like target spot and early blight.",
        "usage": "Apply as a foliar spray at the first sign of infection."
    },
    "A7": {
        "name": "Chlorothalonil",
        "description": "Protects against fungal diseases like late blight, early blight, and septoria leaf spot.",
        "usage": "Apply as a protective fungicide spray every 7–10 days."
    },
    "A8": {
        "name": "Mancozeb",
        "description": "Broad-spectrum fungicide for fungal diseases like leaf mold and target spot.",
        "usage": "Use as a foliar spray; ensure thorough coverage of leaves."
    },
    "A9": {
        "name": "Neem Oil",
        "description": "Organic treatment for pests and diseases like spider mites and yellow leaf curl virus.",
        "usage": "Spray on affected areas to deter pests and manage mild infections."
    },
    "A10": {
        "name": "Abamectin",
        "description": "Miticide effective against spider mites.",
        "usage": "Apply as a foliar spray to the undersides of leaves for maximum effect."
    },
}

# Map disease IDs to suitable antibiotic IDs
disease_antibiotic_mapping = {
    0: ["A1", "A2", "A3"],  # Bacterial Spot
    1: ["A6", "A7", "A8"],  # Early Blight
    2: ["A3"],             # Healthy (No antibiotics needed, but copper may help as a preventive measure)
    3: ["A3", "A7"],       # Late Blight
    4: ["A8", "A7"],       # Leaf Mold
    5: ["A7", "A8"],       # Septoria Leaf Spot
    6: ["A6", "A8"],       # Target Spot
    7: ["A9", "A2"],       # Yellow Leaf Curl Virus
    8: ["A2", "A3"],       # Tomato Mosaic Virus
    9: ["A9", "A10"],      # Two-Spotted Spider Mite
}

# Get antibiotics based on disease ID
def get_antibiotics_for_disease(disease_id):
    antibiotic_ids = disease_antibiotic_mapping.get(disease_id, [])
    return [antibiotic_data[a_id] for a_id in antibiotic_ids]

# Improved translation function with error handling
def translate_text(text, target_lang):
    if target_lang == "ta":
        try:
            translated = translator.translate(text, dest="ta")
            return translated.text if translated else text
        except Exception:
            print("Translation failed, returning original text.")
            return text  # Fallback to English if translation fails
    return text  # Default to English

# Flask route for antibiotics display with language support
@app.route('/antibiotics/<int:disease_id>')
def antibiotics(disease_id):
    lang = request.args.get("lang", "en")  # Default language is English
    antibiotics = get_antibiotics_for_disease(disease_id)

    if antibiotics:
        translated_antibiotics = deepcopy(antibiotics)  # Avoid modifying original data

        if lang == "ta":
            for antibiotic in translated_antibiotics:
                antibiotic["description"] = translate_text(antibiotic["description"], "ta")
                antibiotic["usage"] = translate_text(antibiotic["usage"], "ta")

        return render_template("antibiotics.html", antibiotics=translated_antibiotics, disease_id=disease_id, lang=lang)
    else:
        return render_template("error.html", message=f"No antibiotics found for Disease ID {disease_id}."), 404

if __name__ == "__main__":
    app.run(debug=True)