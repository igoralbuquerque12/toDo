from django.shortcuts import render
from .models import Task
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

def redirecionar(request, task_id=None):
    if (task_id == None):
        if request.method == 'GET':
            return listar(request)
        elif request.method == 'POST':
            return gravar(request) 
    else: 
        if request.method == 'GET':
            return listar_uma_tarefa(request, task_id)
        elif request.method == 'DELETE':
            return deletar_task(request, task_id) 
        elif request.method == 'PATCH':
            return update_task(request, task_id)

def listar(request):
    try:
        tasks = Task.objects.all()
        tasks_list = [{ "id": task.id, "titulo": task.title } for task in tasks]
        return JsonResponse({ "status": "success", "data": tasks_list }, status=200)
    except Exception as e:
        return JsonResponse({ "status": "fail", "message": str(e) }, status=400)

# @csrf_exempt
def gravar(request):
    try:
        data = json.loads(request.body)
        title = data.get("title")
        description = data.get("description", "")

        if not title:
            return JsonResponse({"status": "fail", "message": "É necessário conter o titulo"}, status=400)

        task = Task.objects.create(title=title, description=description)
        return JsonResponse({"status": "success", "task_id": task.id}, status=201)
    except Exception as e:
        return JsonResponse({ "status": "fail", "message": str(e) }, status=400)

def listar_uma_tarefa(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task_data = {"id": task.id, "title": task.title, "description": task.description, "completed": task.completed}
        return JsonResponse({ "status": "success", "data": task_data }, status=200)
    except Task.DoesNotExist:
        return JsonResponse({ "status": "fail", "message": "Task não encontrada" }, status=404)
    except Exception as e:
        return JsonResponse({ "status": "fail", "message": str(e) }, status=400)
    
def deletar_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.delete()
        return JsonResponse({ "status": "success", "message": f"Task {task_id} deletada com sucesso" }, status=200)
    except Task.DoesNotExist:
        return JsonResponse({ "status": "fail", "message": "Task não encontrada para ser deletada" }, status=404)
    except Exception as e:
        return JsonResponse({ "status": "fail", "message": str(e) }, status=400)
    
def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id) 
    except Task.DoesNotExist: 
        return JsonResponse({"status": "fail", "message": "Task não encontrada"}, status=404)

    try:
        new_data = json.loads(request.body) 
        task.title = new_data.get("title", task.title)  
        task.description = new_data.get("description", task.description)
        task.completed = new_data.get("completed", task.completed)

        task.save()  
        return JsonResponse({
            "status": "success",
            "message": f"Dados da task {task.id} alterados com sucesso"
        }, status=200)
    except Exception as e:
        return JsonResponse({"status": "fail", "message": str(e)}, status=400)  