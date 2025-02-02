
BASE = "https://www.ebay.fr/sch/i.html?"
MAX_PAGINATION = 1000

def build(search: str, pagination: int = 240, page: int = 1, extra: str = None) -> str:
    assert(isinstance(search, str))
    assert(isinstance(pagination, int))
    assert(isinstance(page, int))
    assert(isinstance(extra, (str, type(None))))

    url: str = BASE
    url += f"_nkw={search.replace(' ', '+')}"
    url += "&" + f"_ipg={min(pagination, MAX_PAGINATION)}"
    url += "&" + f"_pgn={page}"

    if extra:
        url += "&" + extra
    
    return url
