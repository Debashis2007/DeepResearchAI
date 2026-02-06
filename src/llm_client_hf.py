"""
Hugging Face LLM Client for Deep Research AI.

This module provides LLM integration using Hugging Face models,
suitable for deployment on Hugging Face Spaces.
"""

import json
import re
from typing import Any

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    import torch
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

try:
    from huggingface_hub import InferenceClient
    HF_INFERENCE_AVAILABLE = True
except ImportError:
    HF_INFERENCE_AVAILABLE = False


class HuggingFaceLLMClient:
    """
    LLM client for Hugging Face models.
    
    Supports both local model loading and Hugging Face Inference API.
    """
    
    # Recommended models for research tasks
    RECOMMENDED_MODELS = {
        "small": "mistralai/Mistral-7B-Instruct-v0.3",
        "medium": "Qwen/Qwen2.5-7B-Instruct", 
        "large": "meta-llama/Llama-3.1-8B-Instruct",
        "best": "microsoft/Phi-3-medium-4k-instruct",
    }
    
    def __init__(
        self,
        model_id: str = "Qwen/Qwen2.5-7B-Instruct",
        use_inference_api: bool = True,
        hf_token: str | None = None,
        device: str = "auto",
        max_new_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> None:
        """
        Initialize the Hugging Face LLM client.
        
        Args:
            model_id: Hugging Face model ID
            use_inference_api: Use HF Inference API (recommended for Spaces)
            hf_token: Hugging Face API token
            device: Device to use ("auto", "cuda", "cpu")
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
        """
        self.model_id = model_id
        self.use_inference_api = use_inference_api
        self.hf_token = hf_token
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        
        self.client = None
        self.pipeline = None
        self.tokenizer = None
        self.model = None
        
        if use_inference_api:
            self._init_inference_client()
        else:
            self._init_local_model(device)
    
    def _init_inference_client(self) -> None:
        """Initialize Hugging Face Inference API client."""
        if not HF_INFERENCE_AVAILABLE:
            raise ImportError(
                "huggingface_hub not installed. "
                "Install with: pip install huggingface_hub"
            )
        
        self.client = InferenceClient(
            model=self.model_id,
            token=self.hf_token
        )
    
    def _init_local_model(self, device: str) -> None:
        """Initialize local model."""
        if not HF_AVAILABLE:
            raise ImportError(
                "transformers not installed. "
                "Install with: pip install transformers torch"
            )
        
        # Determine device
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_id,
            token=self.hf_token
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            token=self.hf_token,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map=device,
            trust_remote_code=True
        )
        
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=self.max_new_tokens,
            temperature=self.temperature,
            do_sample=True,
        )
    
    async def call(self, prompt: str, system_prompt: str | None = None) -> str:
        """
        Call the LLM with a prompt.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            Generated text response
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        if self.use_inference_api:
            return await self._call_inference_api(messages)
        else:
            return self._call_local_model(messages)
    
    async def _call_inference_api(self, messages: list[dict]) -> str:
        """Call using Inference API."""
        import asyncio
        
        # Run in executor since client is sync
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.chat_completion(
                messages=messages,
                max_tokens=self.max_new_tokens,
                temperature=self.temperature,
            )
        )
        
        return response.choices[0].message.content
    
    def _call_local_model(self, messages: list[dict]) -> str:
        """Call local model."""
        # Format messages for the model
        if hasattr(self.tokenizer, "apply_chat_template"):
            prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
        else:
            # Fallback formatting
            prompt = ""
            for msg in messages:
                role = msg["role"]
                content = msg["content"]
                if role == "system":
                    prompt += f"System: {content}\n\n"
                elif role == "user":
                    prompt += f"User: {content}\n\nAssistant: "
        
        outputs = self.pipeline(prompt, return_full_text=False)
        return outputs[0]["generated_text"]
    
    async def call_json(
        self,
        prompt: str,
        system_prompt: str | None = None
    ) -> dict[str, Any]:
        """
        Call LLM and parse JSON response.
        
        Args:
            prompt: User prompt (should request JSON output)
            system_prompt: Optional system prompt
            
        Returns:
            Parsed JSON as dictionary
        """
        # Add JSON instruction to prompt
        json_prompt = prompt + "\n\nRespond with valid JSON only."
        
        response = await self.call(json_prompt, system_prompt)
        
        return self._parse_json_response(response)
    
    def _parse_json_response(self, response: str) -> dict[str, Any]:
        """Parse JSON from response text."""
        # Try direct parse
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from markdown code blocks
        json_patterns = [
            r'```json\s*([\s\S]*?)\s*```',
            r'```\s*([\s\S]*?)\s*```',
            r'\{[\s\S]*\}',
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, response)
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
        
        # Return empty dict if parsing fails
        return {"raw_response": response, "parse_error": True}


# Factory function
def create_hf_client(
    model_size: str = "medium",
    use_inference_api: bool = True,
    hf_token: str | None = None
) -> HuggingFaceLLMClient:
    """
    Create a Hugging Face LLM client.
    
    Args:
        model_size: "small", "medium", "large", or "best"
        use_inference_api: Use Inference API (recommended)
        hf_token: Hugging Face token
        
    Returns:
        Configured HuggingFaceLLMClient
    """
    model_id = HuggingFaceLLMClient.RECOMMENDED_MODELS.get(
        model_size,
        HuggingFaceLLMClient.RECOMMENDED_MODELS["medium"]
    )
    
    return HuggingFaceLLMClient(
        model_id=model_id,
        use_inference_api=use_inference_api,
        hf_token=hf_token
    )
