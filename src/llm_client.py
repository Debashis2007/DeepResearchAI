"""
LLM client for interacting with language models.
"""

import json
import logging
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod

from openai import OpenAI
from anthropic import Anthropic

from .config import config

logger = logging.getLogger(__name__)


class BaseLLMClient(ABC):
    """Base class for LLM clients."""
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> str:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """Generate a JSON response from the LLM."""
        pass


class OpenAIClient(BaseLLMClient):
    """OpenAI API client."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or config.llm.api_key
        self.model = model or config.llm.model
        self.client = OpenAI(api_key=self.api_key)
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> str:
        """Generate a response from OpenAI."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or config.llm.temperature,
            "max_tokens": max_tokens or config.llm.max_tokens,
        }
        
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        
        try:
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """Generate a JSON response from OpenAI."""
        # Add JSON instruction to prompt
        json_prompt = prompt + "\n\nRespond with valid JSON only."
        
        response = await self.generate(
            prompt=json_prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            json_mode=True
        )
        
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            # Try to extract JSON from response
            return self._extract_json(response)
    
    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Extract JSON from text that might contain other content."""
        # Try to find JSON block
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start != -1 and end > start:
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass
        
        return {"error": "Failed to parse response", "raw": text}


class AnthropicClient(BaseLLMClient):
    """Anthropic API client."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or config.llm.fallback_api_key
        self.model = model or config.llm.fallback_model
        self.client = Anthropic(api_key=self.api_key)
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> str:
        """Generate a response from Anthropic."""
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens or config.llm.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        
        if system_prompt:
            kwargs["system"] = system_prompt
        
        if temperature is not None:
            kwargs["temperature"] = temperature
        
        try:
            response = self.client.messages.create(**kwargs)
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
    
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """Generate a JSON response from Anthropic."""
        json_prompt = prompt + "\n\nRespond with valid JSON only, no other text."
        
        response = await self.generate(
            prompt=json_prompt,
            system_prompt=system_prompt,
            temperature=temperature
        )
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                try:
                    return json.loads(response[start:end])
                except json.JSONDecodeError:
                    pass
            return {"error": "Failed to parse response", "raw": response}


class LLMClient:
    """Main LLM client with fallback support."""
    
    def __init__(self):
        self.primary = OpenAIClient()
        self.fallback = AnthropicClient()
        self._use_fallback = False
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> str:
        """Generate a response with fallback support."""
        client = self.fallback if self._use_fallback else self.primary
        
        try:
            return await client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                json_mode=json_mode
            )
        except Exception as e:
            if not self._use_fallback:
                logger.warning(f"Primary LLM failed, trying fallback: {e}")
                self._use_fallback = True
                return await self.generate(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    json_mode=json_mode
                )
            raise
    
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """Generate a JSON response with fallback support."""
        client = self.fallback if self._use_fallback else self.primary
        
        try:
            return await client.generate_json(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature
            )
        except Exception as e:
            if not self._use_fallback:
                logger.warning(f"Primary LLM failed, trying fallback: {e}")
                self._use_fallback = True
                return await self.generate_json(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature
                )
            raise


# Global LLM client instance
llm_client = LLMClient()
