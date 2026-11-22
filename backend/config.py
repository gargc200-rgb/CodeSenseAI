"""
Configuration module for CodeSense AI
Course: Prompt Engineering (SCSE4041) - Milestone 2
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"
DOCS_DIR = BASE_DIR / "docs"
EXPERIMENTS_DIR = BASE_DIR / "experiments"

# API Keys (loaded securely from environment)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# Default LLM settings
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "auto") # auto, gemini, openai, mock
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-3.5-flash")
GEMINI_FALLBACK_MODELS = ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.6-flash", "gemini-3-flash-preview"]
FALLBACK_OPENAI_MODEL = os.getenv("FALLBACK_OPENAI_MODEL", "gpt-4o-mini")

# Supported Programming Languages
SUPPORTED_LANGUAGES = ["Python", "C++", "Java"]

# Available Prompts
PROMPT_VERSIONS = {
    "P1": {
        "id": "P1",
        "name": "Baseline Prompt",
        "file": "baseline_prompt.txt",
        "description": "Basic unstructured instruction asking for error identification without role or pedagogical constraints."
    },
    "P2": {
        "id": "P2",
        "name": "Improved Prompt",
        "file": "improved_prompt.txt",
        "description": "Introduces instructor role, severity classification, beginner-friendly explanations, and basic anti-leakage constraints."
    },
    "P3": {
        "id": "P3",
        "name": "Final Optimized Prompt",
        "file": "final_prompt.txt",
        "description": "Full prompt engineering architecture: Role prompting, context prompting, task decomposition, few-shot exemplars, strict JSON schema, and strict zero-leakage guardrails."
    }
}

DEFAULT_PROMPT_VERSION = "P3"

# Request Limits
MAX_CODE_LENGTH_CHARS = 10000
MAX_DESCRIPTION_LENGTH_CHARS = 2000
API_TIMEOUT_SECONDS = int(os.getenv("API_TIMEOUT_SECONDS", "30"))
