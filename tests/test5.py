from dataclasses import dataclass

@dataclass
class Container:
    id: str
    value: float


data = ["03b", 32.03]

print(*data)
print(Container(*data))