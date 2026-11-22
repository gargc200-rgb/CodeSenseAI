"""
Prompt Management Module for CodeSense AI
Handles loading, caching, variable injection, and prompt versioning.
"""
from pathlib import Path
from typing import Dict, Any, Optional
from backend.config import PROMPTS_DIR, PROMPT_VERSIONS

class PromptManager:
    def __init__(self, prompts_dir: Path = PROMPTS_DIR):
        self.prompts_dir = prompts_dir
        self._prompt_cache: Dict[str, str] = {}
        self._load_all_prompts()

    def _load_all_prompts(self) -> None:
        """Load and cache prompt template files from disk."""
        for version_id, meta in PROMPT_VERSIONS.items():
            file_path = self.prompts_dir / meta["file"]
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    self._prompt_cache[version_id] = f.read()
            else:
                raise FileNotFoundError(f"Required prompt template not found: {file_path}")

    def get_prompt_text(self, version_id: str) -> str:
        """Retrieve the raw template text for a prompt version."""
        version_id = version_id.upper()
        if version_id not in self._prompt_cache:
            raise KeyError(f"Unknown prompt version '{version_id}'. Valid versions: {list(PROMPT_VERSIONS.keys())}")
        return self._prompt_cache[version_id]

    def format_prompt(
        self,
        version_id: str,
        language: str,
        code: str,
        problem_description: Optional[str] = None
    ) -> str:
        """
        Format a prompt template with the provided language, code, and optional context.
        """
        raw_template = self.get_prompt_text(version_id)
        
        context_block = ""
        if problem_description and problem_description.strip():
            context_block = f"Student's Intended Goal / Problem Context:\n{problem_description.strip()}\n"

        formatted = raw_template.format(
            language=language,
            code=code,
            context_block=context_block
        )
        return formatted

    def get_version_info(self, version_id: str) -> Dict[str, Any]:
        """Return metadata for a specific prompt version."""
        version_id = version_id.upper()
        if version_id not in PROMPT_VERSIONS:
            raise KeyError(f"Unknown prompt version '{version_id}'.")
        info = dict(PROMPT_VERSIONS[version_id])
        info["template_length"] = len(self.get_prompt_text(version_id))
        return info

    def list_versions(self) -> Dict[str, Dict[str, Any]]:
        """List all available prompt versions and their metadata."""
        result = {}
        for vid in PROMPT_VERSIONS:
            result[vid] = self.get_version_info(vid)
        return result

# Global singleton instance
prompt_manager = PromptManager()
