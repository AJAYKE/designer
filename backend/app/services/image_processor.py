import re
from typing import List, Dict, Any
from html import escape
from app.models.design_state import UnsplashImage

# Treat common blanks and ANY data-URI images as placeholders
IMG_PLACEHOLDER = (
    r'(?:'
    r'placeholder|'                # literal "placeholder"
    r'#|'                          # "#"
    r'about:blank|'                # about:blank
    r'data:image/(?:gif|png|jpeg|jpg|svg\+xml)'  # any inline data-uri img
    r')'
)

AI_IMG_SELECTOR = r'\bdata-ai-img\s*=\s*["\']([^"\']+)["\']'
AI_BG_SELECTOR  = r'\bdata-ai-bg\s*=\s*["\']([^"\']+)["\']'

class ImageProcessor:
    def extract_image_requirements(self, html: str) -> List[Dict[str, Any]]:
        """
        Extract what images we need to fetch. We look for:
        - <img ... src|data-src=PLACEHOLDER ...> (+ alt | nearest heading)
        - style="background-image:url(PLACEHOLDER)"
        - Tailwind arbitrary background class bg-[url(PLACEHOLDER)]
        - Explicit hints via data-ai-img / data-ai-bg to craft better queries
        """
        reqs: List[Dict[str, Any]] = []

        # <img src="placeholder|data:" ... alt="...">  (also supports data-ai-img)
        for m in re.finditer(
            rf'<img[^>]+(?:src|data-src)=["\']{IMG_PLACEHOLDER}[^"\']*["\'][^>]*>',
            html, re.I
        ):
            tag = m.group(0)
            kind = self._match_attr(tag, AI_IMG_SELECTOR) or "image"
            alt  = self._attr(tag, "alt") or self._guess_context_label(html, m.start())
            q    = self._query(alt or kind)
            reqs.append({"query": q, "type": "img", "kind": kind})

        # inline style background-image (also supports data-ai-bg on same element)
        for m in re.finditer(
            rf'(<[^>]+(?:{AI_BG_SELECTOR})?[^>]*style=["\'][^"\']*background-image\s*:\s*url\(\s*["\']?{IMG_PLACEHOLDER}[^)\'"]*["\']?\s*\)[^"\']*["\'][^>]*>)',
            html, re.I
        ):
            tag = m.group(1)
            kind = self._match_attr(tag, AI_BG_SELECTOR) or "background"
            label = self._guess_context_label(html, m.start()) or kind
            q = self._query(label)
            reqs.append({"query": q, "type": "background", "kind": kind, "width": 1600, "height": 900})

        # Tailwind arbitrary bg: bg-[url('#'|data:image:...)]
        # We can’t easily set inline style here without parsing, so we still fetch an image
        # and later replace the class AND (optionally) add/patch a style attribute via regex.
        if re.search(r'bg-\[url\(\s*["\']?'+IMG_PLACEHOLDER+r'[^)\']*["\']?\s*\)\]', html, re.I):
            reqs.append({"query": "modern ui hero", "type": "background", "kind": "tailwind-bg", "width": 1600, "height": 900})

        # Cap to a sane max
        return reqs[:8]

    def inject_images(self, html: str, images: List[UnsplashImage]) -> str:
        if not images:
            return html

        pool = images[:]  # copy so we can pop

        # Replace <img ... src=placeholder> (ALL matches)
        def repl_img(m):
            nonlocal pool
            tag = m.group(0)
            if not pool:
                return tag
            img = pool.pop(0)
            tag = re.sub(r'(?:src|data-src)=["\'].*?["\']', f'src="{img.url}"', tag, flags=re.I)
            # add perf + alt if missing
            if re.search(r'\bloading=', tag, re.I) is None:
                tag = tag[:-1] + ' loading="lazy" decoding="async">'
            if re.search(r'\balt=', tag, re.I) is None:
                tag = tag[:-1] + f' alt="{escape(img.alt_description or "Image")}">'
            # widths/heights are optional; we leave user-provided values intact
            return tag

        html = re.sub(
            rf'<img[^>]+(?:src|data-src)=["\']{IMG_PLACEHOLDER}[^"\']*["\'][^>]*>',
            repl_img, html, flags=re.I
        )

        # Replace ALL inline style background placeholders, cycling through pool
        def repl_bg_inline(m):
            nonlocal pool
            prefix = m.group(1)  # captures `(style="... background-image: `
            if not pool:
                return m.group(0)
            bg = pool.pop(0)
            return re.sub(
                rf'url\(\s*["\']?{IMG_PLACEHOLDER}[^)\'"]*["\']?\s*\)',
                f'url({bg.url})',
                m.group(0),
                flags=re.I
            )

        html = re.sub(
            rf'((?:style)=["\'][^"\']*background-image\s*:\s*)url\(\s*["\']?{IMG_PLACEHOLDER}[^)\'"]*["\']?\s*\)',
            repl_bg_inline, html, flags=re.I
        )

        # Tailwind arbitrary bg: replace class and add inline style if possible
        # 1) Replace class token with sane defaults
        html = re.sub(
            r'(class=["\'][^"\']*)\b(bg-\[url\([^\]]+\)\])',
            r'\1 bg-cover bg-center',
            html, flags=re.I
        )
        # 2) If pool still has images, add a style="background-image:url(...)" next to class
        #    For safety, do a light-weight approach: when we see a class=..., if the tag has no style= with background,
        #    inject one (single best-effort per tag).
        def add_inline_style(m):
            nonlocal pool
            before = m.group(1)
            rest   = m.group(2)
            if not pool:
                return m.group(0)
            if re.search(r'style=["\'][^"\']*background-image\s*:', rest, re.I):
                return m.group(0)
            bg = pool.pop(0)
            # inject a style attr before closing '>'
            if 'style=' in rest:
                return m.group(0)  # already has a style (even if not background); avoid risking breakage
            return before + ' style="background-image:url(' + bg.url + ')"' + rest

        html = re.sub(
            r'(<[^>]*class=["\'][^"\']*bg-cover[^"\']*bg-center[^"\']*["\'])([^>]*>)',
            add_inline_style,
            html, flags=re.I
        )

        return html

    # helpers
    def _attr(self, tag: str, name: str) -> str:
        m = re.search(rf'\b{name}\s*=\s*["\']([^"\']+)["\']', tag, re.I)
        return m.group(1).strip() if m else ""

    def _match_attr(self, tag: str, pattern: str) -> str:
        m = re.search(pattern, tag, re.I)
        return m.group(1).strip() if m else ""

    def _query(self, alt: str) -> str:
        if not alt:
            return "modern ui hero"
        stop = {"image", "photo", "picture", "of", "the", "a", "an", "for", "and"}
        words = [w for w in re.split(r'\s+', alt.lower()) if w and w not in stop]
        return " ".join(words[:5]) or "modern ui hero"

    def _guess_context_label(self, html: str, idx: int) -> str:
        # look ~200 chars back for a heading or CTA
        window = html[max(0, idx-300):idx]
        m = re.search(r'<h[1-3][^>]*>([^<]{3,120})</h[1-3]>', window, re.I)
        if m:
            return m.group(1).strip()
        c = re.search(r'<a[^>]*>([^<]{3,120})</a>', window, re.I)
        return (c.group(1).strip() if c else "website hero")
