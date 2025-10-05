# Atlas / ARES Brand System

This folder stores lightweight assets and guidance for the Atlas / ARES black-and-gold identity. All files tracked in git are vector sources so the repository stays friendly to Git and satisfies the binary-free constraint.

## Usage Principles

1. **Contrast first:** always place the gold accents (#E5B80B) on the charcoal background (#0B0B0E) or a neutral slate (#1A1B22) for maximum contrast.
2. **Typography:** headings use the geometric sans vibe of **Poppins** (Streamlit will fall back to Segoe UI), while body copy uses **Inter** for clarity.
3. **Padding:** keep at least the width of the gold accent bar around the logo when placing it on a background. This roughly equals the height of the wordmark.
4. **Accessibility:** maintain a contrast ratio of 4.5:1 for text. When in doubt, use the atlas-white tone for body copy against black backgrounds.

## File Overview

- `atlas_logo.svg` – Primary wordmark (black background friendly)
- `atlas_logo_invert.svg` – Gold and white treatment for dark backgrounds
- `atlas_logo_mono.svg` – Single-color variant for embossing or engravings
- `atlas_avatar.svg` – Circular avatar/monogram for favicons and profile chips
- `theme.css` – CSS variables consumed by Streamlit pages for consistent styling
- `modules/*.svg` – Reserved marks for sibling assistants (ARES, Orion, Red AI)
- `generated/` – Created by `python scripts/build_assets.py`; contains PNG and ICO exports (ignored by git)

## Do / Do Not

**Do**
- Pair the gold accent with ample negative space.
- Use the mono mark when printing in a single color.
- Tint hover states or outlines using a translucent gold.
- Regenerate PNG/ICO exports with `make assets` whenever the SVGs change.

**Do Not**
- Stretch or skew the wordmark.
- Place the gold text over busy photographic backgrounds without blur.
- Change the accent color unless prototyping a new brand exploration.

## EDIT HERE: Custom Themes
If you would like to experiment with alternative colors, duplicate `theme.css` and adjust the `:root` variables. Update `.streamlit/config.toml` so Streamlit picks up the new palette.
