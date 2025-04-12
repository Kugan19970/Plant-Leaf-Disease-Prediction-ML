import pandas as pd
from googletrans import Translator

# Load seasonal tips from an Excel file
SEASONAL_TIPS_FILE = "seasonal_tips.xlsx"

def load_seasonal_tips():
    try:
        df = pd.read_excel(SEASONAL_TIPS_FILE)
        df.columns = df.columns.str.strip()  # Remove extra spaces in column names
        return df.set_index("Season")["Tips"].to_dict()  # Convert to dictionary with season as key
    except Exception as e:
        print(f"Error loading seasonal tips: {e}")
        return {}

# Load seasonal tips into memory
SEASONAL_TIPS = load_seasonal_tips()

# Dummy Database for Disease-Based Video Tutorials
DISEASE_VIDEOS = {
    (0, 9): "https://www.youtube.com/embed/7FMB4FaiWTE?si=bLK9KW7Z9O8k5SD5",
    (10, 19): "https://www.youtube.com/embed/XxZVQKsAaBo",
}

# Initialize the Google Translate API
translator = Translator()

def get_video_url(disease_id):
    """Get the YouTube video URL for the given disease_id."""
    try:
        disease_id = int(disease_id)
        for (start, end), url in DISEASE_VIDEOS.items():
            if start <= disease_id <= end:
                return url
    except ValueError:
        return "Invalid disease ID"
    
    return "No video available for this disease."

def get_seasonal_advice(season, language):
    """Get seasonal advice and translate it if necessary."""
    advice = SEASONAL_TIPS.get(season, "No seasonal advice available.")

    if language != 'en':
        try:
            advice = translator.translate(advice, src='en', dest=language).text
        except Exception as e:
            advice = f"Translation Error: {e}"

    return advice
