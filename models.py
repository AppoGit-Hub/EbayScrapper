from dataclasses import dataclass

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
class Offer:
    id: str
    date: str
    title: str
    type: str
    is_new: str
    star: float
    subtitle: str
    price: float
    pseudo: str
    sales_count: int
    satisfaction: float
    bid_count: int
    purchase: str
    shipping: str
    country: str

@dataclass
class ScrapStats:
    skipped: int = 0

@dataclass
class RunStats:
    total: int = 0
    exist: int = 0
    added: int = 0
  

class StatsSingleton:
    _stats = None
    def get_instance() -> ScrapStats:
        if StatsSingleton._stats is None:
            StatsSingleton._stats = ScrapStats()
        return StatsSingleton._stats

    def reset():
        StatsSingleton._stats = None