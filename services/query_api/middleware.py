import json
import logging
import sys
import time
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Configure logging to output to stdout with ONLY the message content
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='%(message)s'
)

class TelemetryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()

        response = await call_next(request)
        
        raw_log = {
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "path": request.url.path,
            "status_code":response.status_code,
            "latency_ms": (time.perf_counter() - start)*1000
        }

        emit_structured_log(raw_log)

        return response
        
def track_llm_call(model: str, prompt_tokens: int, completion_tokens: int, temperature: float, latency_ms:float, tenant_id: str) -> dict:
    return {
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
        "temperature": temperature,
        "llm_latency": latency_ms,
        "tenant_id": tenant_id
    }


def emit_structured_log(log_payload: dict) -> None:
    logging.info(json.dumps(log_payload))
