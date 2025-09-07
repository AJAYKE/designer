from app.models.design_state import DesignState
from app.services.unsplash_service import UnsplashService
from app.services.image_processor import ImageProcessor

async def image_enhancer(state: DesignState) -> DesignState:
    """
    Image enhancement agent - finds and replaces placeholder images with Unsplash (or robust fallbacks).
    """
    print(f"🖼️ Image Enhancement Agent: Processing images for {state.get('thread_id','unknown')}")
    
    try:
        html_code = state["html_code"]
        image_processor = ImageProcessor()
        requirements = image_processor.extract_image_requirements(html_code)

        if not requirements:
            return {**state, "images": [], "status": "complete", "progress": 75}

        unsplash = UnsplashService()
        fetched = []

        # Fetch per requirement to improve topical match (hero vs cards, etc.)
        for req in requirements:
            try:
                imgs = await unsplash.search_images(
                    query=req.get("query") or "modern ui hero",
                    count=1,
                    width=req.get("width"),
                    height=req.get("height"),
                    orientation="landscape" if req.get("type") == "background" else "landscape"
                )
                if imgs:
                    fetched.extend(imgs)
            except Exception as img_error:
                print(f"⚠️ Image search failed for '{req.get('query')}': {img_error}")
                continue

        # Replace placeholders with actual image URLs (now supports multi-replace)
        enhanced_html = image_processor.inject_images(html_code, fetched)

        # Fire-and-forget download tracking for Unsplash images
        for img in fetched:
            if getattr(img, "download_location", ""):
                try:
                    await unsplash.track_download(img.download_location)
                except Exception:
                    pass

        return {
            **state,
            "html_code": enhanced_html,
            "images": fetched,
            "status": "complete",
            "progress": 90
        }
        
    except Exception as e:
        print(f"❌ Image Enhancement Agent Error: {str(e)}")
        return {
            **state,
            "images": [],
            "status": "complete",
            "progress": 75,
            "error_message": f"Image enhancement failed: {str(e)} (proceeding without images)"
        }
