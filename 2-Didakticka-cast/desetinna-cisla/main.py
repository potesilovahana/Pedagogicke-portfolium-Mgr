"""Spouštěcí bod aplikace Desetinná čísla."""
from __future__ import annotations

import pygame

from game_manager import GameManager
from settings import Settings


def main() -> None:
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        pass
    try:
        GameManager(Settings.load()).run()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
