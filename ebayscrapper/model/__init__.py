#STD
from dataclasses import dataclass
from typing import Optional
from datetime import date
from abc import ABC, abstractmethod

@dataclass
class GenericDataclass:
    pass

@dataclass
class WebsiteConfig:
    filename: str
    wait_time: int
    update_interval: int
    url: str

@dataclass
class MailCredential:
    sender: str
    password: str
    receiver: str

@dataclass 
class PostgressCredential:
    dbname: str
    user: str
    password: str
    host: str
    port: str

@dataclass
class Model(ABC):
    @abstractmethod
    def exist(self) -> bool:
        pass

@dataclass
class PurchaseCategory(Model):
    name: str

    def exist(self) -> bool:
        return self.name is not None

@dataclass
class Country(Model):
    name: str

    def exist(self) -> bool:
        return self.name is not None

@dataclass
class Author(Model):
    id: int
    pseudo: str
    country: Country

    def exist(self) -> bool:
        return self.id is not None

@dataclass
class Satisfaction(Model):
    author: Author
    date: date
    value: float

    def exist(self) -> bool:
        return self.author.exist() and self.date is not None

@dataclass
class BidCount(Model):
    author: Author
    date: date
    value: float

    def exist(self) -> bool:
        return self.author.exist() and self.date is not None

@dataclass
class SalesCount(Model):
    author: Author
    date: date
    value: int

    def exist(self) -> bool:
        return self.author.exist() and self.date is not None

@dataclass
class Star(Model):
    value: float

    def exist(self) -> bool:
        return self.value is not None

@dataclass
class Offer:
    id: str
    date: date
    title: str
    subtitle: Optional[str]
    price: float
    shipping: str
    purchase: Optional[PurchaseCategory]
    star: Optional[Star]
    author: Author

    def exist(self) -> bool:
        return self.id is not None


@dataclass
class ScrapStats:
    skipped: int = 0
    exist: int = 0
    added: int = 0

    def get_total(self) -> int:
        return self.skipped + self.exist + self.added

class ScrapStatsSingleton:
    _stats = None
    def get_instance() -> ScrapStats:
        if ScrapStatsSingleton._stats is None:
            ScrapStatsSingleton._stats = ScrapStats()
        return ScrapStatsSingleton._stats

    def reset():
        ScrapStatsSingleton._stats = None