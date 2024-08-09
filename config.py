# config.py
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    # Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Twitter
    TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    # LLM Providers
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    # Application settings
    TABLE_NAME = 'papers'
    BOT_NAME = 'AI Agent [Alpha Testing]'
    TEMPLATE_PATH = 'prompts/system_en.prompt'
    SLEEP_TIME = 43200  # 12 hours in seconds

    # Default LLM provider
    # DEFAULT_LLM_PROVIDER = 'anthropic'
    # MODEL = 'claude-3-5-sonnet-20240620'
    
    DEFAULT_LLM_PROVIDER = 'openai'
    MODEL = 'gpt-4o'

    @classmethod
    def get_llm_api_key(cls, provider: Optional[str] = None) -> str:
        provider = provider or cls.DEFAULT_LLM_PROVIDER
        if provider == 'openai':
            return cls.OPENAI_API_KEY
        elif provider == 'anthropic':
            return cls.ANTHROPIC_API_KEY
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    @classmethod
    def validate(cls):
        required_vars = [
            'SUPABASE_URL', 'SUPABASE_KEY',
            'TWITTER_CONSUMER_KEY', 'TWITTER_CONSUMER_SECRET',
            'TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_TOKEN_SECRET',
        ]
        
        # Check if at least one LLM provider key is set
        if not (cls.OPENAI_API_KEY or cls.ANTHROPIC_API_KEY):
            raise ValueError("At least one LLM provider API key (OPENAI_API_KEY or ANTHROPIC_API_KEY) must be set")

        missing = [var for var in required_vars if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

# Validate configuration on import
Config.validate()