"""Načítání a ukládání uživatelského nastavení."""
from __future__ import annotations
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from constants import SETTINGS_FILE

@dataclass
class Settings:
    volume: float = 0.7
    fullscreen: bool = False
    font_size: int = 26
    lesson_length: int = 10

    @classmethod
    def load(cls, path: Path = SETTINGS_FILE) -> "Settings":
        defaults = cls()
        try:
            raw: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
            value = cls(float(raw.get("volume", defaults.volume)), bool(raw.get("fullscreen", defaults.fullscreen)), int(raw.get("font_size", defaults.font_size)), int(raw.get("lesson_length", defaults.lesson_length)))
            value.volume = max(0.0, min(1.0, value.volume))
            if value.font_size not in (20, 24, 28, 32): value.font_size = defaults.font_size
            if value.lesson_length not in (10, 20, 30, 50): value.lesson_length = defaults.lesson_length
            return value
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return defaults

    def save(self, path: Path = SETTINGS_FILE) -> None:
        try:
            path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            pass
