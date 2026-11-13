"""Teoretický obsah aplikace."""
from dataclasses import dataclass

@dataclass(frozen=True)
class WorkedExample:
    first: str
    operator: str
    second: str
    result: str

THEORY_PARAGRAPHS = (
    "Desetinná čísla používáme, když potřebujeme vyjádřit část celku. Například 2,5 znamená dvě celé a pět desetin.",
    "Při sčítání a odčítání zapisujeme čísla pod sebe. Jednotky patří pod jednotky a desetinné řádky pod sebe.",
    "Když má jedno číslo méně desetinných míst, můžeme na jeho konec dopsat nuly. Hodnota se nezmění: 4,6 = 4,60.",
)
IMPORTANT_RULE = "Desetinné čárky zapisujeme pod sebe."
WORKED_EXAMPLES = (
    WorkedExample("12,35", "+", "4,60", "16,95"),
    WorkedExample("8,40", "+", "0,35", "8,75"),
    WorkedExample("15,60", "−", "3,20", "12,40"),
    WorkedExample("9,70", "−", "1,35", "8,35"),
    WorkedExample("21,05", "+", "2,95", "24,00"),
)
