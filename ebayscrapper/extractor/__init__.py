#STD
import re
import unicodedata
from typing import Optional

#EXTERN
from bs4 import Tag, ResultSet

def pseudo(seller_info) -> Optional[str]:
    if (isinstance(seller_info, Tag)):
        pseudo, _, _ = seller_info.text.split(" ")
        return pseudo
    elif seller_info is not None:
        raise Exception(f"type {type(seller_info)} not supported with {seller_info}")

def sales_count(seller_info) -> Optional[int]:
    if (isinstance(seller_info, Tag)):
        _, sales_count, _ = seller_info.text.split(" ")
        return int(unicodedata.normalize("NFKD", sales_count)[1:-1].replace(" ", ""))
    elif seller_info is not None:
        raise Exception(f"type {type(seller_info)} not supported with {seller_info}")

def satisfaction(seller_info) -> Optional[float]:
    if (isinstance(seller_info, Tag)):
        _, _, satisfaction = seller_info.text.split(" ")
        return float(satisfaction[:-1].replace(",", "."))
    elif seller_info is not None:
        raise Exception(f"type {type(seller_info)} not supported with {seller_info}")

def purchase(purchase) -> Optional[str]:
    if (isinstance(purchase, Tag)):
        return purchase.text
    elif (isinstance(purchase, str)):
        return purchase
    elif purchase is not None:
        raise Exception(f"type {type(purchase)} not supported with {purchase}")

def id(id) -> Optional[str]:
    if isinstance(id, str):
        if "item" in id:
            return id[len("item"):]
        return id
    elif id is not None:
        raise Exception(f"type {type(id)} not supported with {id}")

def is_new(is_new) ->  Optional[str]:
    if (isinstance(is_new, Tag)):
        return is_new.text
    elif (isinstance(is_new, str)):
        return is_new
    elif is_new is not None:
        raise Exception(f"type {type(is_new)} not supported with {is_new}")

def title(title) -> Optional[str]:
    if (isinstance(title, Tag)):
        #TODO : delete 'Nouvelle Annonce'
        return title.text
    elif (isinstance(title, str)):
        return title
    elif title is not None:
        raise Exception(f"type {type(title)} not supported with {title}")
    
def star(star_root) -> Optional[float]:
    if isinstance(star_root, Tag):
        filled = star_root.find_all("svg", class_="icon icon--star-filled-16")
        half = star_root.find_all("svg", class_="icon icon--star-half-16-colored")

        if not isinstance(filled, ResultSet):
            filled = []

        if not isinstance(half, ResultSet):
            half = []

        return len(filled) + (len(half) * 0.5)
    elif star_root is not None:
        raise Exception(f"type {type(star_root)} not supported with {star_root}")

def subtitle(subtitle) -> Optional[str]:
    if (isinstance(subtitle, Tag)):
        return subtitle.text
    elif (isinstance(subtitle, str)):
        return subtitle
    elif subtitle is not None:
        raise Exception(f"type {type(subtitle)} not supported with {subtitle}")

def price(price) -> Optional[float]:
    if (isinstance(price, Tag)):
        text = unicodedata.normalize("NFKD", price.text)
        if "à" in text:
            matchs: list = re.findall(r'\d+\.\d{2}', text.replace(",", "."))
            return sum([float(extract) for extract in matchs]) / len(matchs)
        else:
            base = text[:-len("EUR")].strip().replace(",", ".")
            return float(base.replace(" ", ""))
    elif (isinstance(price, str)):
        return float(price)
    elif price is not None:
        raise Exception(f"type {type(price)} not supported with {price}")

def bid_count(bid_count) -> Optional[int]:
    if (isinstance(bid_count, Tag)):
        return int(''.join(re.findall(r'\d+', bid_count.text)))
    elif (isinstance(bid_count, str)):
        return int(bid_count)
    elif bid_count is not None:
        raise Exception(f"type {type(bid_count)} not supported with {bid_count}")

def shipping(shipping) -> Optional[str]:
    if (isinstance(shipping, Tag)):
        has_price = re.findall(r'\d{1,2},\d{2}', shipping.text)
        if len(has_price) > 0:
            return ''.join(has_price).replace(",", ".")
        else:
            return shipping.text
    elif (isinstance(shipping, str)):
        return shipping
    elif shipping is not None:
        raise Exception(f"type {type(shipping)} not supported with {shipping}")

def country(country) -> Optional[str]:
    if (isinstance(country, Tag)):
        return country.text.split(" ")[1].strip()
    elif (isinstance(country, str)):
        return country
    elif country is not None:
        raise Exception(f"type {type(country)} not supported with {country}")