"""Generate raster brand assets from source SVG files.

This script keeps the git repository free of binary artifacts by creating them on demand.
It converts the maintained SVGs under ``brand/`` into PNG and ICO files that Streamlit and
Windows shortcuts can reuse.

"""Generate raster assets from the SVG sources.

Run manually via ``python scripts/build_assets.py`` or indirectly through ``make assets``.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, Tuple

BRAND_DIR = Path(__file__).resolve().parents[1] / "brand"
GENERATED_DIR = BRAND_DIR / "generated"

ATLAS_BLACK = "#0B0B0E"
ATLAS_GOLD = "#E5B80B"
ATLAS_INK = "#C9CCD6"


def ensure_dependencies() -> None:
    """Verify that optional image libraries are available before proceeding."""

    try:
        import cairosvg  # noqa: F401
    except ImportError as exc:  # pragma: no cover - import guard
        raise SystemExit(
            "cairosvg is required. Install it with `pip install cairosvg` and rerun the script."
        ) from exc

    try:
        from PIL import Image  # noqa: F401
    except ImportError as exc:  # pragma: no cover - import guard
        raise SystemExit(
            "Pillow is required. Install it with `pip install pillow` and rerun the script."
        ) from exc


def svg_to_png(svg_path: Path, png_path: Path, *, scale: float = 1.0, size: Tuple[int, int] | None = None) -> None:
    """Convert an SVG file to a PNG bitmap using cairosvg."""

    from cairosvg import svg2png

    png_path.parent.mkdir(parents=True, exist_ok=True)
    kwargs: dict[str, float | int | str] = {"url": svg_path.as_uri()}
    if size:
        width, height = size
        kwargs["output_width"] = int(width * scale)
        kwargs["output_height"] = int(height * scale)
    png_bytes = svg2png(**kwargs)
    png_path.write_bytes(png_bytes)


def png_to_ico(png_path: Path, ico_path: Path, sizes: Iterable[Tuple[int, int]]) -> None:
    """Render a PNG into an ICO container for Windows shortcuts."""

    from PIL import Image

    ico_path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(png_path)
    image.save(ico_path, sizes=list(sizes))


def generate_logo_assets() -> None:
    """Create standard PNG and ICO exports of the Atlas logo."""

    svg_path = BRAND_DIR / "atlas_logo.svg"
    if not svg_path.exists():  # pragma: no cover - guard for custom forks
        raise SystemExit(f"Missing source SVG: {svg_path}")

    png_path = GENERATED_DIR / "atlas_logo_512.png"
    svg_to_png(svg_path, png_path, size=(512, 512))
    ico_path = GENERATED_DIR / "atlas_icon.ico"
    png_to_ico(png_path, ico_path, sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])


def generate_splash() -> None:
    """Create a simple branded splash background for desktop shortcuts."""

    from PIL import Image, ImageDraw, ImageFont

    width, height = 1280, 720
    image = Image.new("RGB", (width, height), ATLAS_BLACK)
    draw = ImageDraw.Draw(image)

    title_font = _load_font(preferred_sizes=(96, 80, 64))
    subtitle_font = _load_font(preferred_sizes=(40, 32, 28))

    title = "ATLAS / ARES"
    subtitle = "Offline-first personal AI"

    title_w, title_h = draw.textsize(title, font=title_font)
    subtitle_w, subtitle_h = draw.textsize(subtitle, font=subtitle_font)

    title_xy = ((width - title_w) / 2, height / 2 - title_h)
    subtitle_xy = ((width - subtitle_w) / 2, title_xy[1] + title_h + 20)

    draw.text(title_xy, title, fill=ATLAS_GOLD, font=title_font)
    draw.text(subtitle_xy, subtitle, fill=ATLAS_INK, font=subtitle_font)

    splash_path = GENERATED_DIR / "atlas_splash_1280x720.png"
    splash_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(splash_path, format="PNG")


def _load_font(*, preferred_sizes: Iterable[int]) -> "ImageFont.FreeTypeFont | ImageFont.ImageFont":
    """Pick a font available on the host system, falling back to Pillow's default."""

    from PIL import ImageFont

    font_candidates = [
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        Path("/Library/Fonts/Arial Bold.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf"),
    ]

    for size in preferred_sizes:
        for candidate in font_candidates:
            if candidate.exists():
                try:
                    return ImageFont.truetype(str(candidate), size)
                except OSError:
                    continue
    return ImageFont.load_default()


def main() -> int:
    """Entrypoint used by ``python scripts/build_assets.py``."""

    ensure_dependencies()
    generate_logo_assets()
    generate_splash()
    print(f"Generated assets in {GENERATED_DIR.relative_to(Path.cwd()) if GENERATED_DIR.exists() else GENERATED_DIR}")
    return 0


if __name__ == "__main__":  # pragma: no cover - script entry
    sys.exit(main())
