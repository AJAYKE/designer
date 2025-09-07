import httpx, random
from typing import List, Optional
from app.models.design_state import UnsplashImage
from app.core.config import settings

APP_NAME = "llm-designer"

PICSUM_SEEDS = [
    "business", "technology", "startup", "office", "abstract", "gradient",
    "city", "workspace", "team", "analytics", "dashboard", "laptop"
]

class UnsplashService:
    def __init__(self):
        self.base_url = "https://api.unsplash.com"
        self.access_key = settings.UNSPLASH_ACCESS_KEY

    async def search_images(
        self, query: str, count: int = 3, width: Optional[int] = None,
        height: Optional[int] = None, orientation: str = "landscape"
    ) -> List[UnsplashImage]:
        # If we have no key, give high-quality placeholders that actually load.
        if not self.access_key:
            return self._get_placeholder_images(count, width, height, query)

        headers = {"Authorization": f"Client-ID {self.access_key}"}
        params = {
            "query": query or "modern ui hero",
            "per_page": max(1, min(count, 10)),
            "orientation": orientation,
            "content_filter": "high",
            "order_by": "relevant"
        }

        results = []
        async with httpx.AsyncClient(timeout=20) as client:
            for attempt in range(2):  # simple retry
                try:
                    r = await client.get(f"{self.base_url}/search/photos", headers=headers, params=params)
                    if r.status_code == 200:
                        data = r.json().get("results", [])
                        results = data if data else []
                        break
                except Exception:
                    if attempt == 1:
                        results = []
                    continue

        if not results:
            return self._get_placeholder_images(count, width, height, query)

        imgs: List[UnsplashImage] = []
        for p in results[:count]:
            urls = p.get("urls", {})
            # Prefer "raw" so we can add quality/format/size params
            base = urls.get("raw") or urls.get("full") or urls.get("regular")
            if not base:
                continue

            # Construct sized URL with modern params
            q = ["auto=format", "q=80"]
            if width:  q.append(f"w={width}")
            if height: q.append(f"h={height}&fit=crop")
            sized = f"{base}{'&' if '?' in base else '?'}" + "&".join(q)

            imgs.append(UnsplashImage(
                id=p["id"],
                url=sized,
                alt_description=p.get("alt_description") or p.get("description") or query,
                width=p.get("width", 1600),
                height=p.get("height", 900),
                author=p["user"]["name"],
                author_username=p["user"]["username"],
                author_profile=f"https://unsplash.com/@{p['user']['username']}?utm_source={APP_NAME}&utm_medium=referral",
                unsplash_link=f"https://unsplash.com/photos/{p['id']}?utm_source={APP_NAME}&utm_medium=referral",
                download_location=p["links"].get("download_location", "")
            ))
        return imgs

    async def track_download(self, download_location: str):
        if not self.access_key or not download_location:
            return
        headers = {"Authorization": f"Client-ID {self.access_key}"}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                await client.get(download_location, headers=headers)
        except Exception:
            pass

    # ---- FALLBACKS ----
    def _get_placeholder_images(self, count: int, width: Optional[int], height: Optional[int], query: Optional[str]) -> List[UnsplashImage]:
        """
        Return **working** placeholders (via picsum.photos) when Unsplash key is missing or search fails.
        """
        w = width or 1600
        h = height or 900
        imgs: List[UnsplashImage] = []
        for i in range(max(1, count)):
            seed = (query or random.choice(PICSUM_SEEDS)).replace(" ", "-")[:40]
            url = f"https://picsum.photos/seed/{seed}-{i}/{w}/{h}"
            imgs.append(UnsplashImage(
                id=f"picsum-{seed}-{i}",
                url=url,
                alt_description=query or "placeholder image",
                width=w, height=h,
                author="Picsum",
                author_username="picsum",
                author_profile="https://picsum.photos/",
                unsplash_link="",
                download_location=""
            ))
        return imgs
