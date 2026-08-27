import os
from dotenv import load_dotenv
from dataclasses import dataclass
from langchain_openai import ChatOpenAI

load_dotenv()

@dataclass(frozen=True)
class Provider:
    name: str
    env_var: str
    is_free: bool
    base_url: str | None
    model:str


providers = [

Provider(
    "OpenAI",
    "OPENAI_API_KEY",
    True,
    None,
    "gpt-4o-mini"
),

]


def select_provider(name: str) -> Provider:
    for provider in providers:
        if os.getenv(provider.env_var):
            return provider
    raise ValueError(f"Provider {name} not found")


def build_chat_model()-> tuple[ChatOpenAI, Provider]:
    provider = select_provider()
    kwargs = {
        "model": provider.model,
        "api_key": os.getenv(provider.env_var),
        "base_url": provider.base_url,
    }

    if provider.base_url:
        kwargs["base_url"] = provider.base_url
    return ChatOpenAI(**kwargs), provider