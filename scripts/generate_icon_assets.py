# -*- coding: utf-8 -*-
"""Разовый генератор цветных PNG-иконок кнопок (v2.5.3 «UI 2.0», дополнение D-2026-11-02-03+).

Рендерит эмодзи Windows-шрифта Segoe UI Emoji (COLR) в цвет через Pillow
(embedded_color=True — GDI-монохром в Tk не поддерживает цветные шрифты,
поэтому иконки даются как картинки). Запуск из корня worktree:
  python scripts/generate_icon_assets.py
Результат — assets/icons/<имя>.png (64×64, RGBA, прозрачный фон). В GitHub не коммитится (scripts/), иконки — коммитятся.
"""
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "icons")
FONT = r"C:\Windows\Fonts\seguiemj.ttf"
SIZE = 32

GLYPHS = {
    "settings": "⚙️",
    "clear_chat": "🧹",
    "history": "📚",
    "memory": "🧠",
    "export": "💾",
    "logout": "🔑",
    "sync_db": "🔄",
    "sync_xwiki": "🌐",
    "diagnostics": "🩺",
    "logs": "📋",
    "trash": "🗑️",
    "ok": "✅",
}

# v2.5.3: эмодзи ⚙️/💾/🗑️ в Segoe UI Emoji серые по дизайну — дуотон-окраска в смысловые цвета
TINTS = {
    "settings": ((40, 90, 150), (120, 190, 240)),
    "export": ((30, 80, 140), (130, 190, 240)),
    "trash": ((150, 40, 40), (240, 160, 160)),
    "logout": ((160, 110, 30), (250, 200, 90)),
}


def _tint(img, dark, light):
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 12:
                continue
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
            px[x, y] = (int(dark[0] + (light[0] - dark[0]) * lum),
                        int(dark[1] + (light[1] - dark[1]) * lum),
                        int(dark[2] + (light[2] - dark[2]) * lum), a)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    font = ImageFont.truetype(FONT, SIZE)
    for name, glyph in GLYPHS.items():
        img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((SIZE / 2, SIZE / 2), glyph, font=font, embedded_color=True, anchor="mm")
        if name in TINTS:
            img = _tint(img, *TINTS[name])
        path = os.path.join(OUT, f"{name}.png")
        img.save(path)
        print(f"OK {name}.png ({os.path.getsize(path)} байт)")


if __name__ == "__main__":
    main()
