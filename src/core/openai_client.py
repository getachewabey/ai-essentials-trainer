import os
import json
from typing import Generator, Any, Type, Optional
from openai import OpenAI
from pydantic import BaseModel
import streamlit as st

class OpenAIClient:
    def __init__(self):
        self._client = None

    def _get_client(self) -> Optional[OpenAI]:
        if self._client:
            return self._client
            
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            api_key = st.session_state.get("openai_api_key")
            
        if api_key:
            self._client = OpenAI(api_key=api_key)
            return self._client
        return None

    def is_configured(self) -> bool:
        return bool(self._get_client())

    def generate_content_stream(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        model_schema: Type[BaseModel],
        model: str = "gpt-4o", 
        temperature: float = 0.5
    ) -> Generator[str, None, BaseModel]:
        """
        Streams content to the UI, then validates against the schema.
        Yields chunks of text. Returns the parsed object at the end.
        """
        client = self._get_client()
        if not client:
            st.error("OpenAI API Key not configured.")
            return None

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # We use standard streaming to show progress, but we need to ensure JSON structure.
        # Strategy: Enforce JSON mode via response_format for correctness, 
        # stream the raw content for UX, then parse the final string.
        # Note: beta.chat.completions.parse does not support stream=True easily with Pydantic yield.
        # So we use standard chat completion with json_object response format if possible, 
        # or just rely on the model schema prompting + json mode.
        
        # For 'Structured Outputs' strict mode, we typically use client.beta.chat.completions.parse
        # But that doesn't stream token-by-token easily for UI feedback in the same way.
        # Hybrid approach: Stream text (so user sees it), accumulate, then Parse.
        
        full_response = ""
        
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            temperature=temperature,
            response_format={"type": "json_object"} # Enforce JSON
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                yield content
        
        # Parse the accumulated JSON
        try:
            # First, try to load as generic JSON to handle potential trailing characters/markdown formatting
            # Often models output ```json ... ```
            cleaned_response = full_response
            if "```json" in full_response:
                cleaned_response = full_response.split("```json")[1].split("```")[0]
            elif "```" in full_response:
                cleaned_response = full_response.split("```")[1].split("```")[0]
            
            data_dict = json.loads(cleaned_response)
            
            # Robustness: Unwrap if the model returned a single root key (e.g. {"lesson": {...}})
            # but we expect the fields directly.
            if isinstance(data_dict, dict) and len(data_dict) == 1:
                first_value = list(data_dict.values())[0]
                if isinstance(first_value, dict):
                    # We assume this is a wrapper and try to use the inner dict
                    data_dict = first_value

            parsed_obj = model_schema(**data_dict)
            yield parsed_obj
        except (json.JSONDecodeError, Exception) as e:
            st.error(f"Failed to parse generated content: {e}")
            st.code(full_response, language="json")
            return None

    def generate_chat_response(
        self,
        system_prompt: str,
        chat_history: list,
        model: str = "gpt-4o",
        temperature: float = 0.7
    ) -> Generator[str, None, None]:
        """Simple chat streaming without schema validation"""
        client = self._get_client()
        if not client:
            st.error("OpenAI API Key not configured.")
            return
            
        messages = [{"role": "system", "content": system_prompt}] + chat_history
        
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            temperature=temperature
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
