"""
CodeSense AI - FastAPI Web Application
Course: Prompt Engineering (SCSE4041) - Milestone 2
"""
import os
import time
from typing import Dict, Any, List
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.config import (
    BASE_DIR,
    PROMPTS_DIR,
    SUPPORTED_LANGUAGES,
    PROMPT_VERSIONS,
    DEFAULT_PROMPT_VERSION,
    DEFAULT_PROVIDER
)
from backend.validator import CodeAnalysisRequest, CodeAnalysisResponse, PromptCompareRequest
from backend.prompt_manager import prompt_manager
from backend.llm_client import llm_client
from backend.response_parser import ResponseParser
from backend.report_generator import ReportGenerator

app = FastAPI(
    title="CodeSense AI",
    description="Educational Code Review Assistant for Beginner Programmers (SCSE4041 - Milestone 2)",
    version="2.0.0"
)

# Enable CORS for local testing & API access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory history cache for the session (last 10 reviews)
ANALYSIS_HISTORY: List[Dict[str, Any]] = []

# Mount static files
frontend_dir = BASE_DIR / "frontend"
static_dir = frontend_dir / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

experiments_dir = BASE_DIR / "experiments"
if experiments_dir.exists():
    app.mount("/experiments-assets", StaticFiles(directory=str(experiments_dir)), name="experiments-assets")

docs_dir = BASE_DIR / "docs"
if docs_dir.exists():
    app.mount("/docs-assets", StaticFiles(directory=str(docs_dir)), name="docs-assets")

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """Serves the main application dashboard."""
    index_path = frontend_dir / "index.html"
    if not index_path.exists():
        return HTMLResponse("<h1>CodeSense AI frontend not found.</h1>", status_code=404)
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/health")
async def health_check():
    """Returns application status, active provider, and loaded prompt versions."""
    active_provider = llm_client.detect_available_provider()
    return {
        "status": "healthy",
        "service": "CodeSense AI",
        "milestone": "Milestone 2 (SCSE4041)",
        "active_provider": active_provider,
        "supported_languages": SUPPORTED_LANGUAGES,
        "available_prompts": list(PROMPT_VERSIONS.keys()),
        "cached_history_count": len(ANALYSIS_HISTORY)
    }

@app.get("/api/prompts")
async def get_prompts():
    """Returns available prompts with metadata and template previews."""
    return {
        "prompts": prompt_manager.list_versions(),
        "default": DEFAULT_PROMPT_VERSION
    }

@app.get("/api/prompts/{version_id}")
async def get_prompt_detail(version_id: str):
    """Returns the full text of a specific prompt template."""
    vid = version_id.upper()
    try:
        text = prompt_manager.get_prompt_text(vid)
        meta = prompt_manager.get_version_info(vid)
        return {
            "version": vid,
            "metadata": meta,
            "template": text
        }
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Prompt version '{version_id}' not found.")

@app.post("/api/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(req: CodeAnalysisRequest):
    """
    Main code review endpoint.
    1. Validates input
    2. Injects variables into selected prompt (P1, P2, P3)
    3. Invokes LLM provider
    4. Parses and validates response schema
    5. Caches history
    """
    prompt_version = (req.prompt_version or DEFAULT_PROMPT_VERSION).upper()
    
    try:
        formatted_prompt = prompt_manager.format_prompt(
            version_id=prompt_version,
            language=req.language,
            code=req.code,
            problem_description=req.problem_description
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to format prompt: {str(e)}")

    raw_output, provider, elapsed_ms = await llm_client.generate_response(
        prompt=formatted_prompt,
        language=req.language,
        prompt_version=prompt_version,
        provider_override=req.provider,
        code=req.code
    )

    parsed_response, is_valid_json = ResponseParser.parse(
        raw_output=raw_output,
        language=req.language,
        prompt_version=prompt_version
    )

    parsed_response.prompt_version_used = prompt_version
    parsed_response.provider_used = provider
    parsed_response.execution_time_ms = elapsed_ms

    # Save to history
    history_entry = {
        "timestamp": time.time(),
        "language": req.language,
        "prompt_version": prompt_version,
        "provider": provider,
        "code_snippet": req.code[:150] + ("..." if len(req.code) > 150 else ""),
        "issue_count": len(parsed_response.issues),
        "overall_assessment": parsed_response.overall_assessment,
        "execution_time_ms": elapsed_ms
    }
    ANALYSIS_HISTORY.insert(0, history_entry)
    if len(ANALYSIS_HISTORY) > 20:
        ANALYSIS_HISTORY.pop()

    return parsed_response

@app.post("/api/compare")
async def compare_prompts(req: PromptCompareRequest):
    """
    Simultaneously runs P1, P2, and P3 on the same code input.
    Enables side-by-side prompt engineering evaluation.
    """
    results = {}
    for vid in ["P1", "P2", "P3"]:
        formatted_prompt = prompt_manager.format_prompt(
            version_id=vid,
            language=req.language,
            code=req.code,
            problem_description=req.problem_description
        )
        raw_output, provider, elapsed_ms = await llm_client.generate_response(
            prompt=formatted_prompt,
            language=req.language,
            prompt_version=vid,
            code=req.code
        )
        parsed, is_json = ResponseParser.parse(raw_output, req.language, vid)
        parsed.prompt_version_used = vid
        parsed.provider_used = provider
        parsed.execution_time_ms = elapsed_ms

        results[vid] = {
            "metadata": prompt_manager.get_version_info(vid),
            "raw_output": raw_output,
            "parsed": parsed.model_dump(),
            "is_valid_json": is_json,
            "execution_time_ms": elapsed_ms
        }

    return {
        "language": req.language,
        "comparison": results
    }

@app.get("/api/history")
async def get_history():
    """Returns recent analysis session history."""
    return {"history": ANALYSIS_HISTORY}

@app.delete("/api/history")
async def clear_history():
    """Clears analysis session history."""
    ANALYSIS_HISTORY.clear()
    return {"message": "History cleared"}

@app.post("/api/export-report")
async def export_report(request: Request):
    """
    Exports the code review results as Markdown or PDF.
    """
    data = await request.json()
    format_type = data.get("format", "markdown").lower()
    code = data.get("code", "")
    student_id = data.get("student_id", "Student")
    problem_description = data.get("problem_description", "")
    analysis_data = data.get("analysis", {})

    try:
        analysis = CodeAnalysisResponse(**analysis_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid analysis payload: {str(e)}")

    if format_type == "pdf":
        pdf_bytes = ReportGenerator.generate_pdf(
            analysis=analysis,
            code=code,
            student_id=student_id,
            problem_description=problem_description
        )
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=CodeSense_Review_Report.pdf"}
        )
    else:
        md_text = ReportGenerator.generate_markdown(
            analysis=analysis,
            code=code,
            student_id=student_id,
            problem_description=problem_description
        )
        return Response(
            content=md_text,
            media_type="text/markdown",
            headers={"Content-Disposition": "attachment; filename=CodeSense_Review_Report.md"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
