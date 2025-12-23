from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from typing import Any, Optional

from .models import BusinessLogicModel
from users.models import BusinessModelComments
from users.forms import ItemCommentForm
from .llm_helper import get_llm_response
import json


def index(request: HttpRequest) -> HttpResponse:
    """
    Renders the main index page of the application.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response for the index page.
    """
    return render(request, 'main/index.html', )


def some_item(request: HttpRequest, item_id: int) -> HttpResponse:
    """
    Renders a specific item's detail page and handles comment submissions.

    Retrieves a `BusinessLogicModel` instance by its ID. If the request method is POST,
    it processes the `ItemCommentForm` to add a new comment linked to the item and the
    current user. Otherwise, it displays the item details and existing comments.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The primary key of the `BusinessLogicModel` item to retrieve.

    Returns:
        HttpResponse: A rendered HTML response containing the item details, comments,
        and the comment form, or a redirect to the same page upon successful comment submission.

    Raises:
        Http404: If the item with the specified `item_id` does not exist (via `get_object_or_404`).
    """
    item = get_object_or_404(BusinessLogicModel, id=item_id)
    item_comments = BusinessModelComments.objects.filter(item=item)

    if request.method == "POST":
        form = ItemCommentForm(request.POST)
        if form.is_valid():
            # Create a comment instance but don't save to DB yet
            comment = form.save(commit=False)
            comment.item_id = item_id
            # Assign the current logged-in user as the author
            comment.author_id = request.user.id
            comment.save()
            return redirect('some_item', id=item_id)
    else:
        form = ItemCommentForm()

    return render(request, 'main/comment_template_XXXXXXX.html', {"form": form, "item_comments": item_comments})


@csrf_exempt
@require_http_methods(["POST"])
def llm_response_view(request: HttpRequest) -> JsonResponse:
    """
    API endpoint to generate a response from an LLM (Large Language Model).

    Expects a JSON payload in the request body with a 'prompt' and optional
    'system_message' and 'temperature'.

    Args:
        request (HttpRequest): The HTTP request object containing the JSON body.

    Returns:
        JsonResponse: A JSON response containing:
            - 'success': Boolean indicating success.
            - 'response': The generated text string from the LLM (if successful).
            - 'error': Error message string (if failed).
            
            Status codes:
            - 200: Success.
            - 400: Invalid JSON or missing 'prompt'.
            - 500: Internal server error during LLM processing.
    """
    try:
        data: dict[str, Any] = json.loads(request.body)
        prompt: Optional[str] = data.get('prompt')
        system_message: Optional[str] = data.get('system_message')
        temperature: float = data.get('temperature', 0.0)

        if not prompt:
            return JsonResponse({'error': 'prompt field is required'}, status=400)

        # Call the helper function to interact with the LLM provider
        response: str = get_llm_response(prompt=prompt, system_message=system_message, temperature=temperature)

        return JsonResponse({'success': True, 'response': response})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)

    except Exception as e:
        # Catch-all for any other errors during processing
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
