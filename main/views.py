from django.shortcuts import render,redirect
from .models import Task

# Renders To Do List main page and passes parameters (if exists) to it
def index(request):
    config = {}
    config['tasks'] = Task.objects.all()
    config['create_status'] = request.session.pop('create_status',None)
    config['delete_status'] = request.session.pop('delete_status',None)
    config['update_status_id'] = request.session.pop('update_status_id',None)
    config['update_status_status'] = request.session.pop('update_status_status',None)
    config['update_name_id'] = request.session.pop('update_name_id',None)
    config['update_name_status'] = request.session.pop('update_name_status',None)

    return render(request, "index.html", config)

# For creating a task
def create(request):
    if request.method == "POST":
        name = request.POST['name']

        duplicates_exist = Task.objects.filter(name = name).count() > 0

        if not duplicates_exist:
            task = Task(name = name)
            task.save()
            request.session['create_status'] = 'Task Successfully Added'
        else:
            request.session['create_status'] = 'Task Already Exists'
    return redirect('index')

# For deleting a task
def delete(request, task_id):
    if request.method == "POST":
        try:
            task = Task.objects.get(id = task_id)
            task_name = task.name
            task.delete()
            request.session['delete_status'] = f"Task {task_name} successfully deleted"
        except Task.DoesNotExist:
            request.session['delete_status'] = f"Task {task_name} failed to delete"
    return redirect('index')

# For updating status of task
def update_status(request, task_id):
    if request.method == "POST":
        try:
            task = Task.objects.get(id = task_id)
            task.status = "Completed" if task.status == "Pending" else "Pending"
            task.save()
            request.session['update_status_id'] = task.id
            request.session['update_status_status'] = f"Task {task.name} updated"
        except Task.DoesNotExist:
            request.session['update_status_status'] = f"Task ID {task_id} does not exist"       
    return redirect('index')

def update_name(request,task_id):
    if request.method == "POST":
        try:
            task = Task.objects.get(id = task_id)
            task.name = request.POST['updated_name']
            task.save()
            request.session['update_name_id'] = task.id
            request.session['update_name_status'] = f"Task Name Updated"
        except Task.DoesNotExist:
            request.session['update_name_status'] = f"Task ID {task_id} does not exist"
    return redirect('index')
