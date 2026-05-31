from fastapi import FastAPI
from pydantic import BaseModel
from services.query_api.auth import create_tenant_jwt, verify_tenant_jwt
import time
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from google import genai
from google.genai import types
from services.query_api.core_rag import build_prompt, execute_inference
from shared.database import fetch_isolated_context
from shared.config import settings


app = FastAPI()
security = HTTPBearer()


class Authorize(BaseModel):
    tenant_id: str
    config: dict

class QueryRequest(BaseModel):
    user_query: str

@app.get("/health")
def get_server_health():
    return {"status": "ok"}

@app.post("/v1/auth/login")
def login(authorize: Authorize):
    return {"token":create_tenant_jwt(authorize.tenant_id,authorize.config)}

@app.post("/v1/query")
async def query(request: QueryRequest, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_tenant_jwt(token)
    
    tenant_id = payload["tenant_id"]
    config = payload["config"]

    start = time.perf_counter()

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    embedding = client.models.embed_content(
        model="gemini-embedding-001",
        contents = [request.user_query],
        config=types.EmbedContentConfig(output_dimensionality=768)
    )

    query_vector = embedding.embeddings[0].values

    relavant_contents = fetch_isolated_context(query_vector, tenant_id)

    prompt = build_prompt(
        config["system_prompt"],
        relavant_contents,
        request.user_query
    )

    response = execute_inference(prompt,config.get("temperature",0.2),config.get("max_tokens",512))

    end = time.perf_counter()

    latency_ms = (end-start) * 1000

    return {
        "response": response,
        "sources": relavant_contents,
        "latency" : latency_ms
    }

