from typing import Optional, TypedDict
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, BaseMessage
from django.conf import settings
import logging, os
from dotenv import load_dotenv


load_dotenv()


class LLMResponse(TypedDict):
    success: bool
    response: Optional[str]
    error: Optional[str]


def get_llm_response(
    prompt: str,
    system_message: Optional[str] = None,
    temperature: float = 0.0
) -> LLMResponse:
    try:
        llm: ChatOpenAI = ChatOpenAI(model="deepseek-chat", openai_api_key=os.getenv('DEEPSEEK_API_KEY'), openai_api_base="https://api.deepseek.com/v1", temperature=temperature, max_tokens=2048)
        messages: list[BaseMessage] = []
        if system_message:
            messages.append(SystemMessage(content=system_message))
        messages.append(HumanMessage(content=prompt))
        response = llm.invoke(messages)
        return {'success': True, 'response': response.content, 'error': None}
    except Exception as e:
        return {'success': False, 'response': None, 'error': str(e)}
