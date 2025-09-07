import os
import asyncio
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from app.models.conversation_state import ConversationState, ConversationPhase
from app.services.llm_service import LLMService
import logging
from app.agents.image_enhancer import image_enhancer
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

def _strip_md_fences(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        s = s.split("\n", 1)[-1]
        if s.endswith("```"):
            s = s[:-3]
    return s.strip()

async def generator(state: ConversationState, config: RunnableConfig, *, store: BaseStore) -> ConversationState:
    """LLM-powered screen generation with parallelism, Unsplash injection, and progress tracking."""
    llm_service = LLMService()

    try:
        plan: Dict[str, Any] = state.get("design_plan") or {}
        screens: List[Dict[str, Any]] = plan.get("screens") or []
        design_system: Dict[str, Any] = plan.get("design_system") or {}

        if not screens:
            return {
                **state,
                "phase": ConversationPhase.ERROR,
                "error_message": "No screens to generate. Please create a design plan first.",
                "updated_at": datetime.utcnow().isoformat(),
            }

        total_screens = len(screens)
        logger.info(f"Starting parallel generation of {total_screens} screens")

        thread_id = config.get("configurable", {}).get("thread_id", "default")

        # initial progress (we’ll keep broadcasting but final return only once)
        generation_progress = {
            "current_screen": 0,
            "total_screens": total_screens,
            "overall_progress": 50,  # 50–95% during work, 100% at end
            "current_screen_name": "",
            "status": "starting",
        }
        if store:
            await store.aput(("generation_progress", thread_id), "current", generation_progress)

        # ---- concurrency controls ----
        # configurable via config.configurable.max_concurrency or env with sane default
        cfg_conc = config.get("configurable", {}).get("max_concurrency")
        max_concurrency = int(cfg_conc or os.getenv("GEN_MAX_CONCURRENCY", "4"))
        sem = asyncio.Semaphore(max_concurrency)

        # track completed count to compute overall %
        completed = 0
        completed_lock = asyncio.Lock()

        async def _broadcast_progress(screen_name: str) -> None:
            # compute a rough 50..95% based on completed
            nonlocal completed
            pct = 50 + int((completed / max(1, total_screens)) * 45)
            progress_payload = {
                "current_screen": completed,
                "total_screens": total_screens,
                "overall_progress": min(pct, 95),
                "current_screen_name": screen_name,
                "status": "generating",
            }
            if store:
                await store.aput(("generation_progress", thread_id), "current", progress_payload)

        async def _generate_one(idx: int, screen_config: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
            screen_title = screen_config.get("title", f"Screen {idx+1}")
            screen_id = screen_config.get("id", f"screen_{idx+1}")

            await _broadcast_progress(screen_title)

            try:
                async with sem:
                    # step 1: code
                    raw_html = await llm_service.generate_screen_code(screen_config, design_system)
                    html_content = _strip_md_fences(raw_html)

                # step 2: enhance (kept outside the same semaphore on purpose in case it hits a different backend;
                # if both hit same rate limit, move this inside the `async with sem:` block)
                enhanced = await image_enhancer({
                    "thread_id": thread_id,
                    "html_code": html_content,
                })
                html_content = enhanced.get("html_code", html_content)
                images = enhanced.get("images", []) or []

                credits = [{
                    "photographer": getattr(img, "author", None),
                    "alt": getattr(img, "alt_description", None),
                    "url": getattr(img, "url", None),
                } for img in images]

                result = {
                    "id": screen_id,
                    "title": screen_title,
                    "screen_type": screen_config.get("screen_type", "landing"),
                    "html": html_content,
                    "css": "",
                    "js": "",
                    "description": screen_config.get("description", ""),
                    "components": screen_config.get("components", []),
                    "credits": credits,
                    "generated_at": datetime.utcnow().isoformat(),
                }

            except Exception as e:
                logger.error(f"Error generating {screen_title}: {e}")
                result = {
                    "id": screen_id,
                    "title": screen_title,
                    "screen_type": screen_config.get("screen_type", "landing"),
                    "html": "",
                    "css": "",
                    "js": "",
                    "description": screen_config.get("description", ""),
                    "components": screen_config.get("components", []),
                    "generated_at": datetime.utcnow().isoformat(),
                    "fallback": True,
                    "error": str(e),
                }
            finally:
                # update shared completion counters + progress
                async with completed_lock:
                    nonlocal completed
                    completed += 1
                    await _broadcast_progress(screen_title)

            return idx, result

        # fan-out
        tasks = [
            asyncio.create_task(_generate_one(i, sc))
            for i, sc in enumerate(screens)
        ]

        # fan-in (keep order by index)
        gathered = await asyncio.gather(*tasks, return_exceptions=False)
        gathered.sort(key=lambda t: t[0])
        generated_screens = [item[1] for item in gathered]

        # finalize progress
        generation_progress.update({
            "current_screen": total_screens,
            "overall_progress": 100,
            "current_screen_name": "Complete",
            "status": "completed",
        })
        if store:
            await store.aput(("generation_progress", thread_id), "current", generation_progress)

        success_screens = [s for s in generated_screens if not s.get("fallback")]
        fallback_screens = [s for s in generated_screens if s.get("fallback")]
        response = (
            f"Generated {len(success_screens)} screens successfully, {len(fallback_screens)} used fallback."
            if fallback_screens else
            f"Successfully generated all {len(generated_screens)} screens!"
        )

        return {
            **state,
            "generated_screens": generated_screens,
            "generation_progress": generation_progress,
            "phase": ConversationPhase.COMPLETE,
            "progress": 100,
            "last_response": response,
            "generation_summary": {
                "total_screens": len(generated_screens),
                "successful_screens": len(success_screens),
                "fallback_screens": len(fallback_screens),
                "completion_time": datetime.utcnow().isoformat(),
                "max_concurrency": max_concurrency,
            },
            "updated_at": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Generator error: {e}")
        return {
            **state,
            "phase": ConversationPhase.ERROR,
            "error_message": f"Screen generation failed: {str(e)}",
            "last_response": "Sorry, there was an error during screen generation. Please try again.",
            "updated_at": datetime.utcnow().isoformat(),
        }
