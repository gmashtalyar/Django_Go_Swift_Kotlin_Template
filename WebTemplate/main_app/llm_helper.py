from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from django.conf import settings
import logging, os
from dotenv import load_dotenv


load_dotenv()


def get_llm_response(prompt, system_message=None, temperature=0.0):
    try:
        llm = ChatOpenAI(model="deepseek-chat", openai_api_key=os.getenv('DEEPSEEK_API_KEY'), openai_api_base="https://api.deepseek.com/v1", temperature=temperature, max_tokens=2048)
        messages = []
        if system_message:
            messages.append(SystemMessage(content=system_message))
        messages.append(HumanMessage(content=prompt))
        response = llm.invoke(messages)
        return {'success': True, 'response': response.content, 'error': None}
    except Exception as e:
        return {'success': False, 'response': None, 'error': str(e)}
