from langdetect import detect


class LanguageDetector:

    def detect_language(
        self,
        text
    ):

        try:

            return detect(
                str(text)
            )

        except:

            return "unknown"