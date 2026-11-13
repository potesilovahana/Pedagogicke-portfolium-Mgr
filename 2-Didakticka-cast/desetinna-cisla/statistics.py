"""Statistiky jedné lekce."""
from dataclasses import dataclass

@dataclass
class LessonStats:
    correct: int = 0
    incorrect: int = 0
    current_streak: int = 0
    best_streak: int = 0

    @property
    def solved(self) -> int:
        return self.correct + self.incorrect

    @property
    def accuracy(self) -> float:
        return self.correct * 100.0 / self.solved if self.solved else 0.0

    def record(self, is_correct: bool) -> None:
        if is_correct:
            self.correct += 1
            self.current_streak += 1
            self.best_streak = max(self.best_streak, self.current_streak)
        else:
            self.incorrect += 1
            self.current_streak = 0
