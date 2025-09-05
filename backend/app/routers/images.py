from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.services.unsplash_service import UnsplashService
from app.models.design_state import UnsplashImage

router = APIRouter()

@router.get("/images/search", response_model=List[UnsplashImage])
async def search_images(
    query: str = Query(..., description="Search query for images"),
    count: int = Query(default=6, ge=1, le=20, description="Number of images to return"),
    width: Optional[int] = Query(default=None, ge=100, le=2000, description="Image width"),
    height: Optional[int] = Query(default=None, ge=100, le=2000, description="Image height"),
    orientation: str = Query(default="landscape", regex="^(landscape|portrait|squarish)$")
):
    """
    Search for images using Unsplash API
    """
    
    try:
        unsplash_service = UnsplashService()
        images = await unsplash_service.search_images(
            query=query,
            count=count,
            width=width,
            height=height,
            orientation=orientation
        )
        
        return images
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image search failed: {str(e)}")

@router.get("/images/trending", response_model=List[UnsplashImage])
async def get_trending_images(
    count: int = Query(default=12, ge=1, le=30, description="Number of trending images to return")
):
    """
    Get trending/popular images from Unsplash
    """
    
    try:
        # Use popular/trending search terms
        trending_queries = [
            "abstract", "technology", "business", "nature", "minimal",
            "architecture", "design", "lifestyle", "workspace", "creative"
        ]
        
        unsplash_service = UnsplashService()
        all_images = []
        
        # Get a few images from each trending category
        images_per_category = max(1, count // len(trending_queries))
        
        for query in trending_queries[:count]:
            category_images = await unsplash_service.search_images(
                query=query,
                count=images_per_category,
                orientation="landscape"
            )
            all_images.extend(category_images)
            
            if len(all_images) >= count:
                break
        
        return all_images[:count]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get trending images: {str(e)}")

@router.get("/images/categories")
async def get_image_categories():
    """
    Get available image categories for the UI
    """
    
    return {
        "categories": [
            {"name": "Abstract", "query": "abstract", "icon": "palette"},
            {"name": "Business", "query": "business professional", "icon": "briefcase"},
            {"name": "Technology", "query": "technology digital", "icon": "cpu"},
            {"name": "Nature", "query": "nature landscape", "icon": "tree-pine"},
            {"name": "Architecture", "query": "architecture building", "icon": "building"},
            {"name": "Lifestyle", "query": "lifestyle people", "icon": "users"},
            {"name": "Food", "query": "food cooking", "icon": "chef-hat"},
            {"name": "Travel", "query": "travel destination", "icon": "plane"},
            {"name": "Creative", "query": "creative art design", "icon": "palette"},
            {"name": "Workspace", "query": "workspace office", "icon": "monitor"}
        ]
    }

