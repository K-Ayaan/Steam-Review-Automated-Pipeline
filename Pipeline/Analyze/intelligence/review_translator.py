import requests
import hashlib
import json
import os


class ReviewTranslator:

    def __init__(self):

        self.url = "http://localhost:11434/api/generate"

        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

        self.cache_file = (
            "data/translation_cache.json"
        )

        if os.path.exists(
            self.cache_file
        ):

            with open(

                self.cache_file,

                "r",

                encoding="utf-8"

            ) as f:

                self.cache = json.load(f)

        else:

            self.cache = {}

    def translate(

        self,

        text

    ):

        text_hash = hashlib.md5(

            text.encode("utf-8")

        ).hexdigest()

        if text_hash in self.cache:

            return self.cache[
                text_hash
            ]
        
        



        prompt = f"""
Translate the following game review into English.

Rules:
- Return translation only.
- No explanations.
- Preserve meaning.
- Keep technical gaming terms.
- If already English, return unchanged.

Review:

{text}
"""

        response = requests.post(

            self.url,

            json={

                "model": self.model,

                "prompt": prompt,

                "stream": False,

                "options": {

                    "temperature": 0

                }
            }
        )

        translated = (

            response.json()

            .get(
                "response",
                text
            )

            .strip()
        )

        self.cache[
            text_hash
        ] = translated

        with open(

            self.cache_file,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                self.cache,

                f,

                ensure_ascii=False,

                indent=2
            )

        return translated