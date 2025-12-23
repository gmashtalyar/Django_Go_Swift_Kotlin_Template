"""
LLM Helper Module.

This module provides utility functions for interacting with Large Language Model (LLM)
APIs, specifically configured to use the DeepSeek API through the LangChain framework.
It abstracts the complexity of setting up and invoking LLM calls, providing a simple
interface for the rest of the application.

Typical usage example:

    response = get_llm_response(
        prompt="What is the capital of France?",
        system_message="You are a helpful geography assistant.",
        temperature=0.5
    )
    if response['success']:
        print(response['response'])
    else:
        print(f"Error: {response['error']}")
"""

from typing import Optional, TypedDict
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, BaseMessage
from django.conf import settings
import logging, os
from dotenv import load_dotenv


# Load environment variables from .env file to access API keys and configuration
load_dotenv()


class LLMResponse(TypedDict):
    """
    Typed dictionary representing the response from an LLM API call.

    This structure provides a consistent format for handling both successful
    responses and error cases from LLM interactions.

    Attributes:
        success: Boolean indicating whether the LLM call completed successfully.
            True if the API returned a valid response, False if an error occurred.
        response: The text content returned by the LLM on success, or None if
            the call failed.
        error: A string describing the error that occurred, or None if the call
            was successful.
    """

    success: bool
    response: Optional[str]
    error: Optional[str]


def get_llm_response(
    prompt: str,
    system_message: Optional[str] = None,
    temperature: float = 0.0
) -> LLMResponse:
    """
    Send a prompt to the DeepSeek LLM and retrieve a response.

    This function creates a ChatOpenAI client configured for the DeepSeek API,
    constructs the appropriate message sequence, and returns the model's response
    in a standardized format.

    Args:
        prompt: The user's input text to send to the LLM. This is the main
            question or instruction for the model to respond to.
        system_message: An optional system-level instruction that sets the
            behavior or persona of the assistant. If provided, it will be
            prepended to the conversation as a SystemMessage.
        temperature: Controls the randomness of the model's output. A value
            of 0.0 produces deterministic responses, while higher values
            (up to 1.0 or 2.0 depending on the model) increase creativity
            and variability. Defaults to 0.0 for consistent outputs.

    Returns:
        LLMResponse: A typed dictionary containing:
            - success (bool): True if the call succeeded, False otherwise.
            - response (Optional[str]): The LLM's response text on success.
            - error (Optional[str]): Error message string on failure.

    Raises:
        No exceptions are raised directly; all exceptions are caught and
        returned in the error field of the response dictionary.

    Example:
        >>> response = get_llm_response(
        ...     prompt="Explain recursion in simple terms.",
        ...     system_message="You are a patient programming tutor.",
        ...     temperature=0.3
        ... )
        >>> if response['success']:
        ...     print(response['response'])

    Note:
        The function requires the DEEPSEEK_API_KEY environment variable to be
        set, either directly in the environment or in a .env file.
    """
    try:
        # Initialize the ChatOpenAI client with DeepSeek API configuration
        llm: ChatOpenAI = ChatOpenAI(
            model="deepseek-chat",
            openai_api_key=os.getenv('DEEPSEEK_API_KEY'),
            openai_api_base="https://api.deepseek.com/v1",
            temperature=temperature,
            max_tokens=2048
        )

        # Build the message list for the conversation
        messages: list[BaseMessage] = []

        # Add system message first if provided (sets assistant behavior/context)
        if system_message:
            messages.append(SystemMessage(content=system_message))

        # Add the user's prompt as a HumanMessage
        messages.append(HumanMessage(content=prompt))

        # Invoke the LLM and get the response
        response = llm.invoke(messages)

        return {'success': True, 'response': response.content, 'error': None}
    except Exception as e:
        # Catch any exceptions (API errors, network issues, etc.) and return
        # them in a standardized error format
        return {'success': False, 'response': None, 'error': str(e)}
