# Brand Guide

## Palette

* `--atlas-black: #0B0B0E`
* `--atlas-gold:  #E5B80B`
* `--atlas-slate: #1A1B22`
* `--atlas-ink:   #C9CCD6`
* `--atlas-white: #F7F7FA`

## Typography

* Headings – Poppins (fallback Segoe UI, Arial, sans-serif)
* Body – Inter (same fallbacks)

## Assets

* `brand/atlas_logo.svg` – Primary wordmark (small caps, gold underline)
* `brand/atlas_logo_mono.svg` – White on black variant
* `brand/atlas_logo_invert.svg` – Gold on black for dark backgrounds
* `brand/atlas_avatar.svg` – Monogram avatar used as favicon/page icon
* `scripts/build_assets.py` – Generate PNG/ICO versions on demand under `brand/generated/`

## Usage

* Streamlit header uses `brand_header.render` with the wordmark and status badges.
* CLI banner prints gold ANSI text defined in `apps/api_fastapi/core/banner.py`.
* Keep sufficient padding (min 24 px) around the logo in UI cards.
* Maintain high contrast (gold on black or white on slate) for accessibility.

## Future modules

* `brand/modules/ares_logo.svg` – Tactical variant for automation tools.
* `brand/modules/orion_logo.svg` – Research-focused variant.
* `brand/modules/redai_logo.svg` – Security/red-team flavour.
