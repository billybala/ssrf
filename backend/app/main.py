from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

from .ssrf import safe_fetch

# Generate basic FastAPI application
app = FastAPI(title="SSRF PoC (Vulnerable + Fixed)")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Endpoint principal
@app.get("/fetch-vuln")
async def fetch_vuln(url: str = Query(..., description="URL a solicitar (vulnerable)")):
    # SSRF: no validación, permite acceder a recursos internos
    
    try:
        r = requests.get(url, timeout=5)
        return {
            "requested_url": url,
            "status_code": r.status_code,
            "content_type": r.headers.get("content-type"),
            "body_preview": r.text[:2000],
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Upstream error: {e}")

@app.get("/fetch-safe")
def fetch_safe(url: str = Query(..., description="URL a solicitar (mitigado)")):
    try:
        result = safe_fetch(url)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Upstream error: {e}")