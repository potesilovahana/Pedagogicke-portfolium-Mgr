"""Načítání a kontrola příkladů z textových souborů."""
from __future__ import annotations
import random
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from constants import DATA_DIR

@dataclass(frozen=True)
class Exercise:
    left_text: str
    operator: str
    right_text: str
    answer: Decimal

    @property
    def question(self) -> str:
        return f"{self.left_text} {self.operator} {self.right_text} = ?"

    @property
    def answer_text(self) -> str:
        value = format(self.answer, "f")
        if "." in value: value = value.rstrip("0").rstrip(".")
        return value.replace(".", ",")

class ExerciseLoader:
    _PATTERN = re.compile(r"([+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+))\s*([+-])\s*([+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+))\s*=\s*([+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+))")

    @staticmethod
    def _decimal(value: str) -> Decimal:
        return Decimal(value.replace(",", "."))

    def load(self, filename: str, data_dir: Path = DATA_DIR) -> list[Exercise]:
        try:
            content = (data_dir / filename).read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueError(f"Soubor s příklady „{filename}“ se nepodařilo načíst.") from exc
        if not content.strip():
            raise ValueError(f"Soubor „{filename}“ je prázdný.")
        exercises: list[Exercise] = []
        for match in self._PATTERN.finditer(content):
            left, op, right, given = match.groups()
            try:
                a, b, expected = (self._decimal(v) for v in (left, right, given))
            except InvalidOperation:
                continue
            if (a + b if op == "+" else a - b) == expected:
                exercises.append(Exercise(left.replace(".", ","), op, right.replace(".", ","), expected))
        if not exercises:
            raise ValueError(f"V souboru „{filename}“ nejsou žádné platné příklady.")
        return exercises

    @staticmethod
    def make_lesson(exercises: list[Exercise], count: int) -> list[Exercise]:
        result: list[Exercise] = []
        while len(result) < count:
            batch = exercises.copy()
            random.shuffle(batch)
            result.extend(batch[:count - len(result)])
        return result
