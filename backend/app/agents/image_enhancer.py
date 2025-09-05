from app.models.design_state import DesignState
from app.services.unsplash_service import UnsplashService
from app.services.image_processor import ImageProcessor

async def image_enhancement_agent(state: DesignState) -> DesignState:
    """
    Image enhancement agent - finds and replaces placeholder images with Unsplash images
    """
    print(f"🖼️ Image Enhancement Agent: Processing images for {state['thread_id']}")
    
    try:
        html_code = state["html_code"]
        
        # Extract image requirements from HTML
        image_processor = ImageProcessor()
        image_requirements = image_processor.extract_image_requirements(html_code)
        
        if not image_requirements:
            # No images needed, proceed to validation
            return {
                **state,
                "images": [],
                "status": "complete",
                "progress": 75
            }
        
        # Search for appropriate images on Unsplash
        unsplash_service = UnsplashService()
        images = []
        
        for requirement in image_requirements:
            try:
                unsplash_images = await unsplash_service.search_images(
                    query=requirement["query"],
                    count=1,
                    width=requirement.get("width", 800),
                    height=requirement.get("height", 600)
                )
                
                if unsplash_images:
                    images.extend(unsplash_images)
                    
            except Exception as img_error:
                print(f"⚠️ Image search failed for '{requirement['query']}': {img_error}")
                continue
        
        # Replace placeholders with actual image URLs
        enhanced_html = image_processor.inject_images(html_code, images)
        
        return {
            **state,
            "html_code": enhanced_html,
            "images": images,
            "status": "complete",
            "progress": 75
        }
        
    except Exception as e:
        print(f"❌ Image Enhancement Agent Error: {str(e)}")
        # Non-critical error - proceed without images
        return {
            **state,
            "images": [],
            "status": "complete",
            "progress": 75,
            "error_message": f"Image enhancement failed: {str(e)} (proceeding without images)"
        }

