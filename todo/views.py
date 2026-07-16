from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods
import json
from todo.models import Task


# Create your views here.
def index(request):
    if request.method == "POST":
        priority = request.POST.get("priority", 3)
        task = Task(title=request.POST["title"],
                    due_at=make_aware(parse_datetime(request.POST["due_at"])),
                    priority=int(priority))
        task.save()

    order_by = request.GET.get("order", "priority")
    if order_by == "due":
        tasks = Task.objects.order_by("due_at")
    elif order_by == "posted":
        tasks = Task.objects.order_by("-posted_at")
    else:  # default to priority
        tasks = Task.objects.order_by("-priority", "-posted_at")

    context = {
        "tasks": tasks
    }
    return render(request, "todo/index.html", context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)


def close(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    task.completed = True
    task.save()

    return redirect(index)


def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == 'POST':
        task.title = request.POST['title']
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
        task.save()
        return redirect(detail, task_id)

    context = {
        'task': task
    }
    return render(request, "todo/edit.html", context)


def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect(index)


@require_http_methods(["POST"])
def update_order(request):
    """Update task order via drag and drop"""
    try:
        data = json.loads(request.body)
        task_ids = data.get('task_ids', [])

        for index, task_id in enumerate(task_ids):
            try:
                task = Task.objects.get(pk=task_id)
                task.order = index
                task.save()
            except Task.DoesNotExist:
                pass

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
