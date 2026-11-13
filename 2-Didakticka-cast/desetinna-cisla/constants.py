"""Společné konstanty aplikace."""
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
ASSETS_DIR = ROOT_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
SETTINGS_FILE = ROOT_DIR / "settings.json"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Desetinná čísla"
BACKGROUND = (245, 248, 255)
WHITE = (255, 255, 255)
INK = (48, 57, 82)
MUTED = (105, 115, 140)
BLUE = (126, 177, 235)
BLUE_DARK = (75, 135, 205)
GREEN = (55, 160, 112)
RED = (222, 91, 103)
PINK = (247, 190, 204)
YELLOW = (255, 224, 135)
LAVENDER = (198, 185, 241)
MINT = (154, 222, 194)
BORDER = (222, 229, 242)
