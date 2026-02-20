from dataclasses import dataclass
@dataclass
class Card:
    card_name:str
    quantita:int

    def __hash__(self):
        return hash(self.card_name)

    def __str__(self):
        return self.card_name