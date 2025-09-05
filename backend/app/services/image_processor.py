import re
from typing import List, Dict, Any
from app.models.design_state import UnsplashImage

class ImageProcessor:
    """Process images in HTML - extract requirements and inject URLs"""
    
    def extract_image_requirements(self, html: str) -> List[Dict[str, Any]]:
        """
        Extract image requirements from HTML placeholders
        Looks for patterns like:
        - <img src="placeholder" alt="description" />
        - <div class="bg-gray-200"> (background placeholders)
        """
        
        requirements = []
        
        # Extract img tags with placeholder sources
        img_pattern = r'<img[^>]*src=["\'](?:placeholder|#)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*>'
        img_matches = re.findall(img_pattern, html, re.IGNORECASE)
        
        for alt_text in img_matches:
            if alt_text.strip():
                requirements.append({
                    "query": self._generate_search_query(alt_text),
                    "alt_text": alt_text,
                    "type": "img"
                })
        
        # Extract background image placeholders (gray boxes that might need images)
        bg_pattern = r'<div[^>]*class=["\'][^"\']*(?:bg-gray-200|bg-gray-300|aspect-video|aspect-square)[^"\']*["\'][^>]*>'
        bg_matches = re.findall(bg_pattern, html, re.IGNORECASE)
        
        # Only add background images for certain layouts
        if len(bg_matches) > 0 and len(requirements) < 3:  # Limit background images
            requirements.append({
                "query": "abstract background",
                "alt_text": "Background image",
                "type": "background",
                "width": 1200,
                "height": 800
            })
        
        return requirements[:5]  # Limit to 5 images max
    
    def inject_images(self, html: str, images: List[UnsplashImage]) -> str:
        """
        Replace image placeholders with actual Unsplash URLs
        """
        
        if not images:
            return html
        
        enhanced_html = html
        
        # Replace img placeholder sources
        def replace_img_placeholder(match):
            if images:
                image = images.pop(0)  # Use first available image
                return match.group(0).replace('src="placeholder"', f'src="{image.url}"').replace('src="#"', f'src="{image.url}"')
            return match.group(0)
        
        enhanced_html = re.sub(
            r'<img[^>]*src=["\'](?:placeholder|#)["\'][^>]*>',
            replace_img_placeholder,
            enhanced_html,
            flags=re.IGNORECASE
        )
        
        # Replace some background placeholders with actual images
        if images:
            bg_image = images[0]
            # Replace first gray background with an image
            enhanced_html = re.sub(
                r'(<div[^>]*class=["\'][^"\']*)(bg-gray-200)([^"\']*["\'][^>]*>)',
                rf'\1bg-cover bg-center\3\n<div style="background-image: url({bg_image.url})" class="absolute inset-0"></div>',
                enhanced_html,
                count=1,
                flags=re.IGNORECASE
            )
        
        return enhanced_html
    
    def _generate_search_query(self, alt_text: str) -> str:
        """
        Generate appropriate Unsplash search query from alt text
        """
        
        # Clean up the alt text
        query = alt_text.lower().strip()
        
        # Remove common words
        stop_words = ["image", "photo", "picture", "of", "the", "a", "an"]
        words = [word for word in query.split() if word not in stop_words]
        
        # Limit to 3 most relevant words
        return " ".join(words[:3]) if words else "abstract"

