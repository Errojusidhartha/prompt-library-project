from django.http import JsonResponse
from .models import Prompt
import json
from django.views.decorators.csrf import csrf_exempt


def prompt_list(request):
    if request.method == "GET":
        data = list(Prompt.objects.all().values())
        return JsonResponse(data, safe=False)

    # ✅ ADD THIS
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def create_prompt(request):
    if request.method == "POST":
        data = json.loads(request.body)

        if len(data['title']) < 3:
            return JsonResponse({"error": "Title too short"}, status=400)

        if len(data['content']) < 20:
            return JsonResponse({"error": "Content too short"}, status=400)

        if not (1 <= data['complexity'] <= 10):
            return JsonResponse({"error": "Invalid complexity"}, status=400)

        Prompt.objects.create(
            title=data['title'],
            content=data['content'],
            complexity=data['complexity']
        )

        return JsonResponse({"message": "Created"})

    # ✅ CRITICAL FIX
    return JsonResponse({"error": "Invalid request"}, status=405)


def prompt_detail(request, id):
    try:
        prompt = Prompt.objects.get(id=id)

        return JsonResponse({
            "id": prompt.id,
            "title": prompt.title,
            "content": prompt.content,
            "complexity": prompt.complexity,
            "views": 0
        })

    except Prompt.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)