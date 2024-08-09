import abc
from typing import List, Dict, Any, Generator, Union, Optional
from openai import OpenAI
import anthropic

class LLMProvider(abc.ABC):
    @abc.abstractmethod
    def generate(self, messages: List[Dict[str, str]], model: str, system: Optional[str] = None, max_tokens: Optional[int] = None, stream: bool = False, **kwargs) -> Union[str, Generator[str, None, None]]:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self):
        self.client = OpenAI()

    def generate(self, messages: List[Dict[str, str]], model: str, system: Optional[str] = None, max_tokens: Optional[int] = None, stream: bool = False, **kwargs) -> Union[str, Generator[str, None, None]]:
        if system:
            messages = [{"role": "system", "content": system}] + messages
        
        if max_tokens:
            kwargs['max_tokens'] = max_tokens

        if stream:
            return self._generate_stream(messages, model, **kwargs)
        else:
            return self._generate_sync(messages, model, **kwargs)

    def _generate_sync(self, messages: List[Dict[str, str]], model: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

    def _generate_stream(self, messages: List[Dict[str, str]], model: str, **kwargs) -> Generator[str, None, None]:
        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            **kwargs
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

class AnthropicProvider(LLMProvider):
    def __init__(self):
        self.client = anthropic.Anthropic()

    def generate(self, messages: List[Dict[str, str]], model: str, system: Optional[str] = None, max_tokens: Optional[int] = None, stream: bool = False, **kwargs) -> Union[str, Generator[str, None, None]]:
        if max_tokens is None:
            raise ValueError("max_tokens is required for Anthropic models")

        anthropic_kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages,
            **kwargs
        }
        if system:
            anthropic_kwargs["system"] = system

        if stream:
            return self._generate_stream(**anthropic_kwargs)
        else:
            return self._generate_sync(**anthropic_kwargs)

    def _generate_sync(self, **kwargs) -> str:
        response = self.client.messages.create(**kwargs)
        return response.content[0].text

    def _generate_stream(self, **kwargs) -> Generator[str, None, None]:
        kwargs["stream"] = True
        stream = self.client.messages.create(**kwargs)
        for event in stream:
            if event.type == "content_block_delta":
                yield event.delta.text

class LLMManager:
    def __init__(self):
        self.providers: Dict[str, LLMProvider] = {
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider()
        }

    def generate(self, messages: List[Dict[str, str]], provider: str, model: str, system: Optional[str] = None, max_tokens: Optional[int] = None, stream: bool = False, **kwargs) -> Union[str, Generator[str, None, None]]:
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")
        return self.providers[provider].generate(messages, model, system, max_tokens, stream, **kwargs)

# Usage example
# if __name__ == "__main__":
#     llm_manager = LLMManager()
    
#     messages = [
#         {"role": "user", "content": "Analyze this dataset for anomalies: <dataset>{{DATASET}}</dataset>"}
#     ]
    
#     system_prompt = "You are a seasoned data scientist at a Fortune 500 company."
    
#     response = llm_manager.generate(
#         messages, 
#         provider="openai", 
#         model="gpt-4o", 
#         stream=True,
#         system=system_prompt
#     )
#     for response in response:
#         print(response, end="", flush=True)
    
#     # Streaming example with Anthropic
#     for token in llm_manager.generate(
#         messages, 
#         provider="anthropic", 
#         model="claude-3-5-sonnet-20240620", 
#         system=system_prompt,
#         max_tokens=1024,
#         stream=True
#     ):
#         print(token, end="", flush=True)
#     print()
