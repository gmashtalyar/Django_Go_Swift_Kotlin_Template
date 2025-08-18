from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import BusinessLogicModel
from users.models import BusinessModelComments
from users.forms import ItemCommentForm
from llm_helper import get_llm_response
import json


def index(request):
    return render(request, 'main/index.html', )


def some_item(request, item_id):
    item = get_object_or_404(BusinessLogicModel, id=item_id)
    item_comments = BusinessModelComments.objects.filter(item=item)
    if request.method == "POST":
        form = ItemCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.item_id = item_id
            comment.author_id = request.user.id
            comment.save()
            return redirect('some_item', id=item_id)
    else:
        form = ItemCommentForm()
    return render(request, 'main/comment_template_XXXXXXX.html', {"form": form, "item_comments": item_comments})


@csrf_exempt
@require_http_methods(["POST"])
def llm_response_view(request):
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt')
        system_message = data.get('system_message')
        temperature = data.get('temperature', 0.0)

        if not prompt:
            return JsonResponse({'error': 'prompt field is required'}, status=400)

        response = get_llm_response(prompt=prompt, system_message=system_message, temperature=temperature)

        return JsonResponse({'success': True, 'response': response})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)

    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
