from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class StoryOptionLLM(BaseModel):
    text: str = Field(description="the text of the option shown to the users")
    score: Dict[str, Any]=  Field(description="the next node content and its option")


class StoryNodeLLM(BaseModel):
    content: str = Field(description="This  is the main content of the story")
    isEnding: bool = Field(description="")
    isWinningEnding: bool = Field("Weather this node is winning ending node")
    options: Optional[List[StoryOptionLLM]] = Field(default=None, description="The option for this node")


class StoryLLMResponse(BaseModel):
    title: str = Field(description="")
    rootNode: StoryNodeLLM = Field(description="")