
BASE = "https://www.ebay.fr/str/"

def build(author_name: str) -> str:
    assert isinstance(author_name, str)

    url: str = BASE
    url += author_name

    return url