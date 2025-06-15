from django.shortcuts import render, get_object_or_404, redirect
from .models import BusinessLogicModel
from users.models import BusinessModelComments
from users.forms import ItemCommentForm


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
