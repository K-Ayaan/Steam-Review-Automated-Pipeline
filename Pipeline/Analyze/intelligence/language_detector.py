from langdetect import detect
from langdetect import DetectorFactory

DetectorFactory.seed = 0


class LanguageDetector:

    def __init__(self):
        
        pass

    def detect_language(
        self,
        text
    ):
        print("LANGUAGE DETECTOR LOADED")
        try:

            text = str(text).strip()

            if not text:

                return "unknown"

            language = detect(text)

            return language

        except:

            return "unknown"