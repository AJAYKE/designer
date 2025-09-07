import time
from typing import Dict, List, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class TokenTracker:
    """Enhanced token usage tracking with analytics"""
    
    def __init__(self):
        self.session_usage = {
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_cost": 0.0,
            "operations": [],
            "start_time": datetime.utcnow(),
            "models_used": set()
        }
        
        # Cost per 1K tokens (approximate GPT-4o-mini pricing)
        self.cost_per_1k = {
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
            "gpt-4o": {"input": 0.005, "output": 0.015},
            "gpt-4": {"input": 0.03, "output": 0.06}
        }
    
    async def track_usage(self, prompt_tokens: int, completion_tokens: int, 
                         model: str, operation_type: str, duration_ms: int,
                         metadata: Dict[str, Any] = None):
        """Track detailed token usage with cost calculation"""
        
        # Calculate costs
        model_costs = self.cost_per_1k.get(model, self.cost_per_1k["gpt-4o-mini"])
        prompt_cost = (prompt_tokens / 1000) * model_costs["input"]
        completion_cost = (completion_tokens / 1000) * model_costs["output"]
        total_cost = prompt_cost + completion_cost
        
        # Update session totals
        self.session_usage["total_prompt_tokens"] += prompt_tokens
        self.session_usage["total_completion_tokens"] += completion_tokens
        self.session_usage["total_cost"] += total_cost
        self.session_usage["models_used"].add(model)
        
        # Record operation details
        operation = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation_type": operation_type,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "cost": total_cost,
            "duration_ms": duration_ms,
            "metadata": metadata or {}
        }
        
        self.session_usage["operations"].append(operation)
        
        # Log usage
        logger.info(
            f"LLM Usage - {operation_type}: "
            f"{prompt_tokens}p + {completion_tokens}c = {prompt_tokens + completion_tokens} tokens, "
            f"${total_cost:.4f}, {duration_ms}ms ({model})"
        )
        
        return operation
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get comprehensive session usage summary"""
        duration = datetime.utcnow() - self.session_usage["start_time"]
        
        # Calculate operation type breakdown
        operation_breakdown = {}
        for op in self.session_usage["operations"]:
            op_type = op["operation_type"]
            if op_type not in operation_breakdown:
                operation_breakdown[op_type] = {
                    "count": 0,
                    "total_tokens": 0,
                    "total_cost": 0.0,
                    "avg_duration": 0
                }
            
            operation_breakdown[op_type]["count"] += 1
            operation_breakdown[op_type]["total_tokens"] += op["total_tokens"]
            operation_breakdown[op_type]["total_cost"] += op["cost"]
            operation_breakdown[op_type]["avg_duration"] += op["duration_ms"]
        
        # Calculate averages
        for op_type in operation_breakdown:
            count = operation_breakdown[op_type]["count"]
            if count > 0:
                operation_breakdown[op_type]["avg_duration"] = int(
                    operation_breakdown[op_type]["avg_duration"] / count
                )
        
        return {
            "session_duration_minutes": duration.total_seconds() / 60,
            "total_operations": len(self.session_usage["operations"]),
            "total_tokens": self.session_usage["total_prompt_tokens"] + self.session_usage["total_completion_tokens"],
            "prompt_tokens": self.session_usage["total_prompt_tokens"],
            "completion_tokens": self.session_usage["total_completion_tokens"],
            "total_cost": self.session_usage["total_cost"],
            "models_used": list(self.session_usage["models_used"]),
            "operation_breakdown": operation_breakdown,
            "cost_per_token": self.session_usage["total_cost"] / max(1, self.session_usage["total_prompt_tokens"] + self.session_usage["total_completion_tokens"]),
            "tokens_per_minute": (self.session_usage["total_prompt_tokens"] + self.session_usage["total_completion_tokens"]) / max(1, duration.total_seconds() / 60)
        }
    
    def get_recent_operations(self, minutes: int = 5) -> List[Dict[str, Any]]:
        """Get operations from the last N minutes"""
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        
        recent_ops = []
        for op in self.session_usage["operations"]:
            op_time = datetime.fromisoformat(op["timestamp"])
            if op_time >= cutoff:
                recent_ops.append(op)
        
        return recent_ops
