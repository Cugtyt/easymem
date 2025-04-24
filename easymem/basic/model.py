"""Model for Basic EasyMem."""

import json

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AsyncAzureOpenAI

from easymem.base.model import ModelBase


class AzureOpenAIClient(ModelBase):
    """A client wrapper for interacting with the Azure OpenAI service."""

    def __init__(self) -> None:
        """Initialize the Azure OpenAI client."""
        super().__init__()
        self.endpoint = "https://smarttsg-gpt.openai.azure.com/"
        self.api_version = "2024-08-01-preview"
        self.model = "gpt-4o"
        self.temperature = 0
        self.token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://cognitiveservices.azure.com/.default",
        )
        self.client = AsyncAzureOpenAI(
            azure_deployment=self.model,
            azure_endpoint=self.endpoint,
            api_version=self.api_version,
            azure_ad_token_provider=self.token_provider,
        )

    def build_messages(self, query: str) -> list[dict]:
        """Build the messages for the Azure OpenAI service."""
        return [
            {
                "role": "system",
                "content": self.system_prompt,
            },
            {
                "role": "user",
                "content": query,
            },
        ]

    async def response(
        self,
        query: str,
        format_model: type,
    ) -> dict:
        """Get a response from the Azure OpenAI service."""
        r = await self.client.beta.chat.completions.parse(
            model=self.model,
            messages=self.build_messages(query), # type: ignore  # noqa: PGH003
            response_format=format_model,
            temperature=self.temperature,
        )
        content_str = r.choices[0].message.content
        if not content_str or not isinstance(content_str, str):
            msg = "Empty response from Azure OpenAI."
            raise ValueError(msg)
        try:
            return json.loads(content_str)
        except json.JSONDecodeError as e:
            msg = f"Failed to parse JSON response: {e}"
            raise ValueError(msg) from e
        except Exception as e:
            msg = f"Unexpected error: {e}"
            raise ValueError(msg) from e
