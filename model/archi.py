from dataclasses import dataclass
@dataclass

class Arco:
    card_a:int
    card_b:int
    peso:int

    def __hash__(self):
        return hash((self.card_a, self.card_b))
    def __str__(self):
        return f"({self.card_a}, {self.card_b})"