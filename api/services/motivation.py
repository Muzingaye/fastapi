from typing import Any, List, Optional
from sqlalchemy.orm import Session
from config import settings
from .. models import post
from .. schemas import story

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser


class Motivation:
    @classmethod
    def __get_llm(cls):
        return ChatOpenAI(model="gpt-4-turbo")

    
    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy"):

        llm = cls.__get_llm()
        story_parser = PydanticOutputParser(pydantic_object=story.CompleteResponse)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                # STORY_PROMPT
                ),
                (
                    "human",
                    f"Create the story with this {theme}"
                )
            ]
        ).partial(format_instructions=story_parser.get_format_instructions())

        raw_response = llm.invoke(prompt.invoke({}))

        response_text = raw_response
        if hasattr(response_text, "content"):
            response_text =  raw_response.content

        story_structure = story_parser.parse(response_text)
        root_node_data =  story_structure.root_node

        # if isinstance(root_node_data,  dict):
        #     root_node_data = StoryNodeLLM.model_validae(root_node_data)
        # cls._process_story_node(db, story.id, root_node_data, is_root=True,)
        cls._process_story_node(db, root_node_data, is_root=True,)
        return root_node_data


    @classmethod
    def _process_story_node( cls, db: Session, node_data: dict[str, Any], is_root: bool = False):
        session = db.SessionLocal()

    # @classmethod
    # def _process_story_node(cls, db: Session,  node_data: dict[str, Any], is_root: bool = False):
    #     pass