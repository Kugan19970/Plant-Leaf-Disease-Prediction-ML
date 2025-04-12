from googletrans import Translator

translator = Translator()
try:
    result = translator.translate("Hello", dest="es")  # Translate to Spanish
    print("Translated Text:", result.text)
except Exception as e:
    print("Error:", str(e))
