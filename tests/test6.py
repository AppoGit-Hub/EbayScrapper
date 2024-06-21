from dataclasses import dataclass, asdict

@dataclass
class Container:
    id: str
    value: int

container = Container('03b', 10.3)
print(asdict(container))