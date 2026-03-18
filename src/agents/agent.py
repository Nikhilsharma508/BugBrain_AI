"""
src/agents/agent.py — LLM Provider Manager
--------------------------------------------
PURPOSE:
    Single place to load any LLM provider (Ollama, ChatGPT, Gemini, OpenRouter).
    All other modules use this to get an LLM client — never import providers directly.

CAPABILITIES:
    - Load any provider: ollama, chatgpt/openai, gemini, openrouter
    - Check if the loaded model supports tool/function calling
    - Get a client with structured output (bound to a Pydantic schema)
    - Graceful fallback: if tool calling is not supported, use plain text + parsing
    - Supports custom model names per provider

EXTENSIBILITY:
    - Add new providers by adding to DEFAULT_MODELS, ENV_VARS, and _load_model()
    - Add Azure OpenAI, Anthropic, etc. with same pattern
    - Add custom base URLs for self-hosted models

CONNECTS TO:
    - extraction_agent.py uses get_client() or get_client_with_structured_output()
    - triage_agent.py uses get_client() or get_client_with_structured_output()
    - Any future agent just imports LLMManager

USAGE:
    from src.agents.agent import LLMManager
    manager = LLMManager(base_model="ollama", specific_model="lfm2.5-thinking:latest")
    llm = manager.get_client()
    # or for structured output:
    llm = manager.get_client_with_structured_output(TriageResult)
"""

import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from typing import Optional, Type

# Load environment variables early for class-level attributes
load_dotenv()

from langchain_openai import ChatOpenAI, AzureChatOpenAI

from langchain_google_genai import ChatGoogleGenerativeAI
from src.telemetry.logger import get_logger

logger = get_logger(__name__)



# Removed static TOOL_CAPABLE_MODELS list in favor of dynamic testing

def _ensure_env_var(var_name: Optional[str]) -> Optional[str]:
    """Ensure the required environment variable exists."""
    if var_name is None:
        return None
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Environment variable '{var_name}' not found.")
    return value

class LLMManager:
    """Unified LLM loader with dynamic tool capability detection."""

    DEFAULT_MODELS = {
        "gemini": _ensure_env_var("GEMINI_MODEL"),
        "openrouter": _ensure_env_var("OPENROUTER_MODEL"),
        "ollama": _ensure_env_var("OLLAMA_MODEL"),
        "azure": _ensure_env_var("AZURE_OPENAI_DEPLOYMENT"),
    }

    ENV_VARS = {
        "gemini": "GEMINI_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
        "ollama": None,
        "azure": "AZURE_OPENAI_API_KEY",
    }

    def __init__(
        self,
        base_model: str = _ensure_env_var("LLM_BASE_MODEL"),
        specific_model: Optional[str] = None,
    ):
        self.base_model = base_model.lower()
        self.specific_model = specific_model or self.DEFAULT_MODELS.get(self.base_model)
        self.temperature = float(_ensure_env_var("LLM_TEMPERATURE") or 0.0)  # Default temperature
        self.max_tokens = _ensure_env_var("LLM_MAX_TOKENS")  # Default max tokens
        
        logger.info(f"LLM active: provider={self.base_model}, model={self.specific_model}")
        
        self.client = self._load_model()


    def _load_model(self):
        """Instantiate the requested LLM client."""
        env_var = self.ENV_VARS.get(self.base_model)
        api_key = _ensure_env_var(env_var)
        

        if self.base_model == "gemini":
            if ChatGoogleGenerativeAI is None:
                raise ImportError("Install langchain-google-genai: pip install langchain-google-genai")
            
            return ChatGoogleGenerativeAI(
                model=self.specific_model,
                temperature=self.temperature,
                google_api_key=api_key,
            )

        if self.base_model == "openrouter":
            if ChatOpenAI is None:
                raise ImportError("Install langchain-openai: pip install langchain-openai")
            return ChatOpenAI(
                model=self.specific_model,
                openai_api_base="https://openrouter.ai/api/v1",
                openai_api_key=api_key,
                temperature=self.temperature,
            )

        if self.base_model == "azure":
            return AzureChatOpenAI(
                azure_endpoint=_ensure_env_var("AZURE_OPENAI_ENDPOINT"),
                api_key=api_key,
                api_version=_ensure_env_var("AZURE_OPENAI_API_VERSION"),
                deployment_name=self.specific_model,
                temperature=self.temperature,
            )

        if self.base_model == "ollama":
            return ChatOllama(
                model=self.specific_model,
                temperature=self.temperature,
            )

        raise ValueError(f"Unsupported base_model: {self.base_model}")

    def get_client(self):
        """Return the loaded LLM client."""
        return self.client

    def supports_tools(self) -> bool:
        """
        Checks if the loaded model supports structured output / tool calling.
        Tests by attempting to bind a schema to the model.
        """
        from pydantic import BaseModel, Field
        import logging
        
        logger = logging.getLogger(__name__)
        
        # Simple test schema
        class TestSchema(BaseModel):
            result: str = Field(description="Test output")
        
        try:
            # If this works, the model supports structured output
            self.client.with_structured_output(TestSchema)
            return True
        except Exception as e:
            logger.debug(f"Model does not support structured output: {e}")
            return False

    def get_client_with_structured_output(self, schema: Type[BaseModel]):
        """Return an LLM client bound to a Pydantic schema for structured output.

        If the model supports tool calling, uses with_structured_output().
        Otherwise, raises a clear error so you know to use a different model
        or handle parsing manually.
        """
        if self.supports_tools():
            return self.client.with_structured_output(schema)
        else:
            raise NotImplementedError(
                f"Model '{self.specific_model}' does not support tool calling. "
                f"Use a tool-capable model or implement manual JSON parsing."
            )


if __name__ == "__main__":
    load_dotenv()
    manager = LLMManager()
    print(f"Model: {manager.specific_model}")
    print(f"Supports tools: {manager.supports_tools()}")