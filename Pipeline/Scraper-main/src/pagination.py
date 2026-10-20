from bs4 import BeautifulSoup


def get_next_page_params(html):

    soup = BeautifulSoup(html, "lxml")
 

    form = soup.find(
        "form",
        id=lambda value:
        value and value.startswith(
            "MoreContentForm"
        )
    )

    if not form:
        return None

    params = {}

    for field in form.find_all("input"):

        name = field.get("name")
        value = field.get("value")

        params[name] = value

    return params