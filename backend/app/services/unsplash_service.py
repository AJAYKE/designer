import httpx
from typing import List, Optional, Dict, Any
from app.models.design_state import UnsplashImage
from app.core.config import settings

class UnsplashService:
    def __init__(self):
        self.base_url = "https://api.unsplash.com"
        self.access_key = settings.UNSPLASH_ACCESS_KEY
        
    async def search_images(
        self, 
        query: str, 
        count: int = 3,
        width: Optional[int] = None,
        height: Optional[int] = None,
        orientation: str = "landscape"
    ) -> List[UnsplashImage]:
        """Search for images on Unsplash"""
        
        if not self.access_key:
            print("⚠️ Unsplash API key not configured, using placeholder images")
            return self._get_placeholder_images(count, width, height)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/search/photos",
                    headers={"Authorization": f"Client-ID {self.access_key}"},
                    params={
                        "query": query,
                        "per_page": count,
                        "orientation": orientation,
                        "content_filter": "high"  # Family-friendly content
                    }
                )
                
                if response.status_code != 200:
                    print(f"⚠️ Unsplash API error: {response.status_code}")
                    return self._get_placeholder_images(count, width, height)
                
                data = response.json()
                images = []
                
                for photo in data.get("results", []):
                    # Determine best size URL
                    image_url = self._get_best_size_url(photo["urls"], width, height)
                    
                    images.append(UnsplashImage(
                        id=photo["id"],
                        url=image_url,
                        alt_description=photo.get("alt_description") or photo.get("description") or query,
                        width=photo["width"],
                        height=photo["height"],
                        author=photo["user"]["name"]
                    ))
                
                return images
                
        except Exception as e:
            print(f"❌ Unsplash search failed: {e}")
            return self._get_placeholder_images(count, width, height)
    
    def _get_best_size_url(self, urls: Dict[str, str], width: Optional[int], height: Optional[int]) -> str:
        """Select the best image size URL based on requirements"""
        
        if width and height:
            return f"{urls['raw']}&w={width}&h={height}&fit=crop"
        elif width:
            return f"{urls['raw']}&w={width}"
        elif height:
            return f"{urls['raw']}&h={height}"
        else:
            return urls.get("regular", urls.get("full"))
    
    def _get_placeholder_images(self, count: int, width: Optional[int] = None, height: Optional[int] = None) -> List[UnsplashImage]:
        """Generate placeholder images when Unsplash is not available"""
        
        w = width or 800
        h = height or 600
        
        images = []
        for i in range(count):
            images.append(UnsplashImage(
                id=f"placeholder-{i}",
                url=f"https://picsum.photos/{w}/{h}?random={i}",
                alt_description="Placeholder image",
                width=w,
                height=h,
                author="Lorem Picsum"
            ))
        
        return images

