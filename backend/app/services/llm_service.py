from textwrap import dedent
import openai
import json
import time
from typing import Dict, Any, AsyncGenerator,Optional
from enum import Enum
from app.core.config import settings
from app.models.conversation_state import ConversationPhase
import logging

from app.services.token_tracker import TokenTracker

logger = logging.getLogger(__name__)

class ScreenType(Enum):
    LANDING = "landing"
    DASHBOARD = "dashboard"
    LOGIN = "login"
    PROFILE = "profile"
    SETTINGS = "settings"
    MOBILE_APP = "mobile_app"
    ECOMMERCE = "ecommerce"
    BLOG = "blog"
    PORTFOLIO = "portfolio"


def _clip_json(obj: Any, limit: int = 4000) -> str:
    try:
        s = json.dumps(obj, ensure_ascii=False)
        return (s[:limit] + "…") if len(s) > limit else s
    except Exception:
        return ""

def _clip(obj: Any, n: int = 3500) -> str:
    try:
        s = json.dumps(obj, ensure_ascii=False)
        return (s[:n] + "…") if len(s) > n else s
    except Exception:
        return ""

class LLMService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL or "gpt-4o-mini"
        self.token_tracker = TokenTracker()
    
    # in LLMService
    async def route_request(self, message: str, current_phase: ConversationPhase, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Phase-aware LLM router. Produces a constrained JSON action for the graph.
        """ 
        import json, time, logging
        logger = logging.getLogger(__name__)
        start = time.time()
        prior = context or {}
        plan_snippet = prior.get("design_plan")
        sys_ctx = ""
        if plan_snippet:
            import json
            sys_ctx = "Context: A prior design plan exists. Consider user may be editing it.\n" \
                    "Keep routing concise.\n" \
                    f"PLAN_SNIPPET={json.dumps(plan_snippet)[:4000]}\n"

        system_prompt = f"""You are a router for a UI/UX design assistant.
        {sys_ctx}
        Always return compact JSON with this exact schema:
        {{"action":"small_talk"|"design_request"|"modification_request"|"cancel"|"noop",
        "confidence":0.0-1.0,
        "reason":"<=15 words",
        "extracted_requirements":"",
        "approval_type":"",
        "modifications":[]
        }}
        Rules:
        - Prefer "modification_request" if a prior plan exists and the user asks for changes.
        - Only use "design_request" for brand new briefs.
        - Be conservative; no hallucinated requirements.
        """


        user_prompt = f"""phase={current_phase.value}
        user="{message}"
        Return only the JSON object per schema; no prose.
        """

        try:
            resp = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}],
                # max_tokens=180,
                # temperature=0.2,
                response_format={"type": "json_object"}
            )

            usage = getattr(resp, "usage", None)
            if usage and hasattr(self, "token_tracker"):
                await self.token_tracker.track_usage(
                    prompt_tokens=usage.prompt_tokens,
                    completion_tokens=usage.completion_tokens,
                    model=self.model,
                    operation_type="routing",
                    duration_ms=int((time.time() - start) * 1000),
                )

            out = json.loads(resp.choices[0].message.content)

            # Minimal post-processing / safety rails
            action = out.get("action") or "noop"
            conf = float(out.get("confidence") or 0.5)

            # Phase gating (belt & suspenders; the graph also enforces this):
            if current_phase != ConversationPhase.INITIAL and action == "design_request":
                # Don’t allow promotion outside INITIAL
                action, conf = "noop", min(conf, 0.6)

            if current_phase != ConversationPhase.AWAITING_APPROVAL and action == "approval_response":
                # Approval only makes sense in AWAITING_APPROVAL
                action, conf = "noop", min(conf, 0.6)

            # Normalize keys
            return {
                "action": action,
                "confidence": conf,
                "reason": out.get("reason", "")[:80],
                "extracted_requirements": out.get("extracted_requirements", "")[:500],
                "approval_type": (out.get("approval_type") or ""),
                "modifications": out.get("modifications") or [],
            }

        except Exception as e:
            logger.error(f"LLM Routing Error: {e}")
            # Very conservative fallback
            return {"action": "noop", "confidence": 0.4, "reason": "fallback", 
                    "extracted_requirements": "", "approval_type": "", "modifications": []}

    

    async def generate_design_plan(self, requirements: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate (or update) a comprehensive design plan using LLM.
        If `context` includes a prior plan and/or a list of modifications, the LLM is instructed
        to update the existing plan in-place, preserving screen IDs and overall style.
        """
        start_time = time.time()
        context = context or {}
        prior_plan          = context.get("prior_plan")
        generated_screens   = context.get("generated_screens")
        modifications       = context.get("modifications") or []

        # ---- System Prompt with explicit UPDATE behavior when context exists ----
        base_schema_prompt = """You are an expert UI/UX designer and system architect. Create comprehensive, actionable design plans.

Respond with JSON containing exactly:
{
  "screens": [
    {
      "id": "unique_id",
      "screen_type": "landing|dashboard|login|profile|settings|mobile_app|ecommerce|blog|portfolio",
      "title": "Screen Title",
      "description": "Brief description of screen purpose and intended visual style (mention gradient, bg-image, and image placements if relevant)",
      "priority": 1-10,
      "order": 1-N,
      "components": [
        "List the main sections AND explicitly note image/visual placements, e.g.: 'Hero with full-bleed image (data-ai-bg=\"hero\")', 'Feature cards each with image (data-ai-img=\"card\")', 'Testimonial avatars (data-ai-img=\"avatar\")'"
      ],
      "interactions": [
        "List concrete motion and micro-interactions with triggers, e.g.: 'staggered fade-in on scroll', 'parallax hero background', 'hover-lift on cards', 'CTA button press ripple', 'smooth in-page scroll'"
      ],
      "data_requirements": [
        "List APIs/data and any image asset slots you expect to be filled later, e.g.: 'hero_image', 'gallery_images[]', 'avatar_image'"
      ]
    }
  ],
  "design_system": {
    "color_scheme": "light|dark|auto",
    "primary_color": "tailwind color name",
    "typography": "modern|classic|minimal",
    "spacing": "compact|comfortable|spacious"
  },
  "generation_strategy": "Detailed, step-by-step build plan including: layout rationale; gradient usage (direction, stops) for sections; where to place background images (mark with data-ai-bg); where to place inline images (mark with data-ai-img); exact animation plan (what animates, when, and how via Tailwind classes and small JS hooks if needed); accessibility and performance notes.",
  "estimated_complexity": "low|medium|high",
  "target_devices": ["desktop", "tablet", "mobile"]
}

Hard Rules:
- Output must be valid JSON (no comments or trailing text).
- Keep the schema exactly as specified (no extra top-level keys).
- Produce MIN 1 and MAX 3 screens total. Choose the most impactful screens for the goals.
- Each screen must call out gradients, background images, and inline images where appropriate.
- Interactions must be specific (e.g., 'fade-in-up with 80ms stagger', 'parallax bg moves slower on scroll').
- Keep 'primary_color' as a Tailwind color token; describe gradients/background images in 'generation_strategy' and the screen text (do NOT invent extra keys).

    """

        # If we have a prior plan, guide the model to UPDATE instead of starting fresh
        update_guidance = ""
        if prior_plan:
            update_guidance = """\n\You are UPDATING an existing plan:
- Preserve the overall visual style and information architecture unless edits conflict.
- **Preserve existing screen IDs** when modifying those screens; reuse IDs to keep downstream references stable.
- Prefer updating existing screens over creating new ones; only add new screens when strictly necessary.
- If a screen is no longer needed, omit it (do not add "removed" flags).
- Keep consistent ordering; adjust `order` to reflect the new sequence.
- Keep `design_system` stable unless edits require changes.
- IMPORTANT: Final result must contain **1–3 screens max**. If the prior plan has more, keep the 2–3 most critical screens for the brief and merge content logically.

    """

        # Compact context snippets to avoid token bloat
        ctx_snippets = []
        if prior_plan:
            ctx_snippets.append("PRIOR_PLAN=" + _clip_json(prior_plan, 5000))
        if generated_screens:
            ctx_snippets.append("GENERATED_SCREENS=" + _clip_json(generated_screens, 4000))
        if modifications:
            ctx_snippets.append("MODIFICATIONS=" + _clip_json(modifications, 1500))

        system_prompt = (
            base_schema_prompt
            + update_guidance
            + ("\n\nContext:\n" + "\n".join(ctx_snippets) if ctx_snippets else "")
        )

        # User prompt includes explicit instruction to apply modifications when present
        if modifications and prior_plan:
            # Edit scenario
            user_prompt = f"""Update the existing design plan based on this brief and the modifications.

Brief:
{requirements}

Apply these modifications precisely (preserve IDs where possible):
{chr(10).join(f"- {m}" for m in modifications)}

Strictly enforce:
- Output 1–3 screens total (pick the most impactful).
- Modern aesthetic with thematic colors, tasteful gradients, and section-level background images where they add clarity.
- Call out explicit image placements using phrases like: hero bg (data-ai-bg="hero"), card image (data-ai-img="card"), avatar (data-ai-img="avatar").
- Rich interactions: scroll-reveal, hover micro-interactions, subtle parallax where suitable; describe timing/stagger clearly.
- Keep JSON schema exact.
- Sort screens by logical flow for the updated experience
    """
        else:
            # New plan or no explicit edits
            user_prompt = f"""Create a design plan for: {requirements}

Constraints & style:
- Produce 1–3 screens total (never more than 3).
- Modern, polished design with a consistent theme and strong visual hierarchy.
- Use tasteful gradients for hero/section backgrounds, and full-bleed background images where appropriate.
- Specify concrete image placements for every visual block (hero, card, avatar, gallery) using descriptive text so generation can create <img> or data-ai-bg later.
- Include robust, explicit animation/micro-interaction plan: scroll reveals (fade/slide/blur with stagger), hover lifts, focus states, smooth in-page scroll; mention durations/delays conceptually.
- Accessibility and performance remain first-class.

Also consider:
- User needs and goals
- Responsive behavior across desktop/tablet/mobile
- WCAG 2.1 AA accessibility
- Performance (lightweight images, lazy-loading hints, minimal JS)
- If a prior plan exists in Context, prefer incremental improvements over a full rewrite.
    """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                # max_tokens=3000,
                # temperature=0.5 if prior_plan or modifications else 0.7,  # tighter variance for updates
                response_format={"type": "json_object"},
            )

            # Track usage
            usage = getattr(response, "usage", None)
            if usage and hasattr(self, "token_tracker"):
                await self.token_tracker.track_usage(
                    prompt_tokens=usage.prompt_tokens,
                    completion_tokens=usage.completion_tokens,
                    model=self.model,
                    operation_type="planning",
                    duration_ms=int((time.time() - start_time) * 1000),
                )

            # Parse and normalize
            plan = json.loads(response.choices[0].message.content)

            # Defensive normalization: ensure required blocks exist
            plan.setdefault("screens", [])
            plan.setdefault("design_system", {})
            plan.setdefault("generation_strategy", "")
            plan.setdefault("estimated_complexity", "medium")
            plan.setdefault("target_devices", ["desktop", "tablet", "mobile"])

            # Ensure IDs exist and sorting is stable
            for i, s in enumerate(plan["screens"]):
                s.setdefault("id", f"screen_{i+1}")
                s.setdefault("order", i + 1)
                s.setdefault("priority", 5)
                s.setdefault("components", [])
                s.setdefault("interactions", [])
                s.setdefault("data_requirements", [])

            # Sort: priority asc, then order asc
            plan["screens"].sort(key=lambda s: (s.get("priority", 5), s.get("order", 999)))

            return plan

        except Exception as e:
            logger.error(f"LLM Planning Error: {e}")
            return self._fallback_plan()
    
    async def process_feedback(self, feedback: str, current_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Process user feedback and modify the plan accordingly"""
        start_time = time.time()
        
        system_prompt = """You are a design plan modifier. Take user feedback and update the design plan accordingly.

Respond with JSON containing:
{
    "action": "approve|modify|cancel",
    "modified_plan": {original plan structure with changes},
    "changes_made": ["list of specific changes"],
    "reasoning": "explanation of modifications"
}"""

        user_prompt = f"""Current plan: {json.dumps(current_plan, indent=2)}

User feedback: "{feedback}"

Modify the plan based on this feedback."""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                # max_tokens=2000,
                # temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            await self.token_tracker.track_usage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                model=self.model,
                operation_type="feedback_processing",
                duration_ms=int((time.time() - start_time) * 1000)
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"LLM Feedback Processing Error: {e}")
            return {"action": "approve", "modified_plan": current_plan, "changes_made": [], "reasoning": "Fallback approval"}
    
    async def generate_screen_code(self, screen_config: Dict[str, Any], design_system: Dict[str, Any]) -> str:
        """Generate complete HTML/CSS/JS code for a specific screen"""
        start_time = time.time()
        screen_type = screen_config.get("screen_type", "landing")
        screen_type = ScreenType(screen_type) if screen_type in ScreenType else ScreenType.LANDING
        max_tokens = self._get_max_tokens_for_screen(screen_type)
        
        system_prompt = self._get_system_prompt_for_screen(screen_type)
        
        user_prompt = f"""Generate a complete, production-ready screen with:

Screen Configuration:
{json.dumps(screen_config, indent=2)}

Design System:
{json.dumps(design_system, indent=2)}

Requirements:
- Single HTML file with inline CSS and JavaScript
- Use only Tailwind CSS utility classes
- Implement all specified components and interactions
- Ensure responsive design and accessibility
- Include realistic placeholder content
- Add smooth animations and micro-interactions"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                # max_tokens=max_tokens,
                # temperature=0.1
            )
            
            await self.token_tracker.track_usage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                model=self.model,
                operation_type=f"generation_{screen_type.value}",
                duration_ms=int((time.time() - start_time) * 1000)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"LLM Screen Generation Error: {e}")
            return self._fallback_screen_html(screen_config.get("title", "Screen"))
    
    async def generate_screen_streaming(
        self, 
        screen_config: Dict[str, Any], 
        design_system: Dict[str, Any]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Generate screen code with streaming support"""
        start_time = time.time()
        screen_type = ScreenType(screen_config.get("screen_type", "landing"))
        max_tokens = self._get_max_tokens_for_screen(screen_type)
        
        system_prompt = self._get_system_prompt_for_screen(screen_type)
        
        user_prompt = f"""Generate a complete, production-ready screen with:

Screen Configuration:
{json.dumps(screen_config, indent=2)}

Design System:
{json.dumps(design_system, indent=2)}

Requirements:
- Single HTML file with inline CSS and JavaScript
- Use only Tailwind CSS utility classes
- Implement all specified components and interactions
- Ensure responsive design and accessibility"""

        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                # max_tokens=max_tokens,
                # temperature=0.4,
                stream=True
            )
            
            accumulated_content = ""
            completion_tokens = 0
            
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    accumulated_content += content
                    completion_tokens += 1
                    
                    yield {
                        "type": "content_delta",
                        "content": content,
                        "accumulated_content": accumulated_content,
                        "screen_id": screen_config.get("id")
                    }
            
            # Estimate tokens for tracking
            prompt_tokens = len(user_prompt.split()) * 1.3
            await self.token_tracker.track_usage(
                prompt_tokens=int(prompt_tokens),
                completion_tokens=completion_tokens,
                model=self.model,
                operation_type=f"streaming_{screen_type.value}",
                duration_ms=int((time.time() - start_time) * 1000)
            )
            
            yield {
                "type": "generation_complete",
                "content": accumulated_content,
                "screen_id": screen_config.get("id"),
                "tokens_used": completion_tokens,
                "duration_ms": int((time.time() - start_time) * 1000)
            }
            
        except Exception as e:
            yield {
                "type": "error",
                "error": str(e),
                "screen_id": screen_config.get("id")
            }
    
    def _get_max_tokens_for_screen(self, screen_type: ScreenType) -> int:
        """Get appropriate max tokens based on screen complexity"""
        token_limits = {
            ScreenType.LANDING: 10000,
            ScreenType.DASHBOARD: 10000,
            ScreenType.LOGIN: 10000,
            ScreenType.PROFILE: 10000,
            ScreenType.SETTINGS: 10000,
            ScreenType.MOBILE_APP: 10000,
            ScreenType.ECOMMERCE: 10000,
            ScreenType.BLOG: 10000,
            ScreenType.PORTFOLIO: 10000
        }
        return token_limits.get(screen_type, 3000)
    
    def _get_system_prompt_for_screen(self, screen_type: ScreenType) -> str:
        base = dedent("""\
            You are an expert frontend developer specializing in modern web development.

            ## Role
            Produce clean, production-ready code and minimal JS for interactions.

            ## Capabilities
            - Semantic HTML5 with proper landmarks and ARIA labels
            - Tailwind CSS utility classes only (no external CSS frameworks)
            - Vanilla JavaScript (no jQuery or frameworks)
            - Mobile-first responsive design
            - WCAG 2.1 AA accessibility compliance
            - Modern layout features (CSS Grid, Flexbox, etc.)

            ## MUST (Hard Rules; do not violate)
            1) Output only a single HTML document in one code block.
            2) Include <html>, <head>, and <body> tags.
            3) Use Tailwind classes only. Any custom CSS must be inline via the style attribute.
            4) Use lucide icons for JavaScript, 1.5 stroke-width.
            5) Start with a short human-readable response line, then the code block, then a short closing response line.
            6) Do not talk about tokens, Tailwind, or HTML in the content (other than the required short responses).
            7) Respect any provided design, code, fonts, colors, and style.
            8) Do not place Tailwind classes on the <html> tag; place them on <body> and descendants.
            9) If charts are required, use Chart.js. Place <canvas> inside a wrapping <div> to prevent infinite growth.
            10) Avoid a bottom-right floating “DOWNLOAD” element.
            11) IMAGES (Strict):
                - Use explicit, semantic placeholders so we can swap them later.
                - For **hero/large visuals** prefer an <img> element over CSS background.
                - If you must use a background image, add data-ai-bg="hero|section|card" AND set style="background-image:url('#')".
                - For <img>, ALWAYS include: src="#" (or data uri), width, height, and meaningful alt text.
                - Also add a data-ai-img="hero|avatar|card|gallery|logo" attribute describing the role.


            ## Style Guidance (Soft, unless user overrides)
            - Modern, minimal, high polish.
            - For tech/cool/futuristic: favor dark mode; for business/professional/traditional: favor light mode.
            - Titles above 20px: tracking-tight.
            - Font weight: use one level thinner (e.g., Bold → Semibold).
            - Add subtle dividers/outlines; tasteful contrast; letter-based logos with tight tracking.
            - Add reveal animations (fade-in, blur-in, slide-in) with staggered delays using Tailwind only (no JS animations).
            - Add hover color and outline interactions.
            - Use custom-styled checkboxes/sliders/dropdowns/toggles only when they are part of the requested UI.

            ## Interactions & Accessibility
            - Provide meaningful focus states and ARIA where appropriate.
            - Keyboard navigability is required.
            - Include validation states, errors, and loading skeletons/spinners where applicable.

            ## Performance & Structure
            - Mobile-first responsive layout.
            - Avoid unnecessary JavaScript; prefer progressive enhancement.
            - Keep DOM semantic and minimal; prefer Grid/Flex for layout.

            ## Output Contract
            - Exactly one fenced code block with the complete HTML document.
            - No extra code blocks.
            - Short response line before and after the code block (human-friendly, not technical).
            - Placeholders MUST be either:
              a) <img src="#" ... data-ai-img="hero|card|avatar|gallery" alt="...">, or
              b) an element with style="background-image:url('#')" and data-ai-bg="hero|section|card".
            - Avoid hotlinking real images. Use ONLY placeholders as above.
            - Provide specific alt text that matches the visual intent (e.g., "Young team collaborating in a modern office", not "image").
            - For cards/grids, include at least 1 image placeholder per distinct visual block where appropriate.
            - For charts, use Chart.js and place <canvas> inside a wrapping <div> to prevent infinite growth.
            - Use Tailwind classes only. Any custom CSS must be inline via the style attribute. <script src="https://cdn.tailwindcss.com"></script>
        """)

        screen_specifics = {
            ScreenType.LANDING: dedent("""\
                ## Screen Focus: Landing
                - Hero with compelling CTAs
                - Feature highlights
                - Testimonials
                - Pricing table
                - Contact form
                - Smooth in-page scrolling and reveal animations
            """),
            ScreenType.DASHBOARD: dedent("""\
                ## Screen Focus: Dashboard
                - KPI cards and data visualizations
                - Interactive charts
                - Sidebar navigation
                - Filtering/search
                - Real-time update states
                - Responsive tables/grids
            """),
            ScreenType.LOGIN: dedent("""\
                ## Screen Focus: Login
                - Secure auth forms
                - Validation and error states
                - Social login placeholders
                - Password reset
                - Loading indicators
            """),
            ScreenType.PROFILE: dedent("""\
                ## Screen Focus: Profile
                - User info display
                - Avatar upload
                - Editable fields
                - Settings tabs
                - Activity history
                - Notification preferences
            """),
            ScreenType.SETTINGS: dedent("""\
                ## Screen Focus: Settings
                - Grouped setting sections
                - Toggles, selectors, validation
                - Save/Cancel actions
                - Confirmation dialogs
            """),
            ScreenType.MOBILE_APP: dedent("""\
                ## Screen Focus: Mobile App
                - Touch-friendly layout
                - Bottom navigation
                - Swipe-like affordances
                - Native-feel interactions
                - Optimized type & spacing
            """),
            ScreenType.ECOMMERCE: dedent("""\
                ## Screen Focus: eCommerce
                - Product catalog and detail pages
                - Search & filters
                - Cart and checkout flow
                - Reviews and ratings
                - Wishlist
            """),
            ScreenType.BLOG: dedent("""\
                ## Screen Focus: Blog
                - Article layouts
                - Category navigation
                - Search
                - Comments section
                - Author profiles
                - Related posts
            """),
            ScreenType.PORTFOLIO: dedent("""\
                ## Screen Focus: Portfolio
                - Project showcases
                - Image galleries
                - Contact form
                - Skills display
                - Timeline layouts
                - Subtle interactive elements
            """),
        }

        return f"{base}\n\n{screen_specifics.get(screen_type, '')}".strip()

    
    async def generate_conversational_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a conversational response for general chat, grounded in current design context when available."""
        start_time = time.time()
        ctx = context or {}
        plan      = ctx.get("design_plan")
        screens   = ctx.get("generated_screens")
        brief     = ctx.get("last_requirements")

        # Build a compact, non-invasive context hint for the model
        ctx_lines = []
        if brief:
            ctx_lines.append("LAST_BRIEF=" + (brief[:600] + "…" if len(brief) > 600 else brief))
        if plan:
            ctx_lines.append("DESIGN_PLAN=" + _clip(plan, 3000))
        if screens:
            # Only feed lightweight metadata to avoid token bloat
            try:
                meta = [
                    {k: s.get(k) for k in ("id","title","screen_type","description")}
                    for s in screens if isinstance(s, dict)
                ]
                ctx_lines.append("GENERATED_SCREENS_META=" + _clip(meta, 2000))
            except Exception:
                pass
        context_blob = ("\n".join(ctx_lines)) if ctx_lines else ""

        system_prompt = """You are a friendly AI design assistant for web/apps.

    Style:
    - Warm, concise, 1–2 sentences max.
    - Helpful and encouraging.
    - If the user asks about the current design, answer using provided context.
    - If they seem stuck, gently suggest next concrete step (one short hint).
    - Do NOT over-explain. Avoid lists, avoid code, avoid emojis unless asked.

    When context is provided:
    - Reference screen titles or plan aspects succinctly (e.g., “hero section”, “pricing”).
    - Do NOT invent features not in context.
    - If user asks to change something, acknowledge and keep it brief (router will handle edits)."""

        user_prompt = (
            f"{message}\n\n"
            + (f"\n[CONTEXT]\n{context_blob}" if context_blob else "")
        )

        try:
            resp = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                # max_tokens=120,
                # temperature=0.6 if context_blob else 0.7,
            )

            usage = getattr(resp, "usage", None)
            if usage and hasattr(self, "token_tracker"):
                await self.token_tracker.track_usage(
                    prompt_tokens=usage.prompt_tokens,
                    completion_tokens=usage.completion_tokens,
                    model=self.model,
                    operation_type="conversational",
                    duration_ms=int((time.time() - start_time) * 1000),
                )

            return (resp.choices[0].message.content or "").strip() or \
                "Happy to help—what would you like to do next?"

        except Exception as e:
            logger.error(f"LLM conversational response error: {e}")
            return "Got it. How can I refine or explain the current design for you?"

    
    def _fallback_routing(self, message: str, phase: ConversationPhase) -> Dict[str, Any]:
        """Fallback routing logic when LLM fails"""
        msg = message.lower()
        
        if phase == ConversationPhase.AWAITING_APPROVAL:
            if any(word in msg for word in ["yes", "approve", "looks good", "perfect"]):
                return {"action": "approval_response", "approval_type": "approve", "confidence": 0.8}
            elif any(word in msg for word in ["change", "modify", "edit", "different"]):
                return {"action": "approval_response", "approval_type": "edit", "confidence": 0.8}
            elif any(word in msg for word in ["cancel", "stop", "abort"]):
                return {"action": "approval_response", "approval_type": "cancel", "confidence": 0.8}
        
        if any(word in msg for word in ["create", "build", "make", "design", "generate"]):
            return {"action": "design_request", "confidence": 0.7, "extracted_requirements": message}
        
        return {"action": "general_chat", "confidence": 0.5}
    
    def _fallback_plan(self) -> Dict[str, Any]:
        """Fallback plan when LLM fails"""
        return {
            "screens": [
                {
                    "id": "landing_01",
                    "screen_type": "landing",
                    "title": "Landing Page",
                    "description": "Main landing page with hero section and features",
                    "priority": 1,
                    "order": 1,
                    "components": ["hero", "features", "cta"],
                    "interactions": ["navigation", "form_submission"],
                    "data_requirements": []
                }
            ],
            "design_system": {
                "color_scheme": "light",
                "primary_color": "blue",
                "typography": "modern",
                "spacing": "comfortable"
            },
            "generation_strategy": "Generate single responsive landing page with modern design",
            "estimated_complexity": "medium",
            "target_devices": ["desktop", "tablet", "mobile"]
        }
    
    def _fallback_screen_html(self, title: str) -> str:
        """Fallback HTML when LLM generation fails"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-gray-50 text-gray-900">
    <header class="bg-white shadow-sm border-b p-6">
        <h1 class="text-2xl font-bold text-gray-900">{title}</h1>
    </header>
    <main class="container mx-auto p-8">
        <div class="bg-white rounded-xl border shadow-sm p-8">
            <h2 class="text-xl font-semibold mb-4">Welcome to {title}</h2>
            <p class="text-gray-600 mb-6">This screen is ready for customization.</p>
            <button class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                Get Started
            </button>
        </div>
    </main>
</body>
</html>"""