import requests


class SteamRequestClient:

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            )
        })

    def get(self, url):
        response = self.session.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.text
    

    def get_homecontent(self, app_id, params):

        url = (
            f"https://steamcommunity.com/app/{app_id}/homecontent/"
        )

        response = self.session.get(
            url,
            params=params,
            timeout=30
        )

        # print(params)

        response.raise_for_status()

        return response.text
    