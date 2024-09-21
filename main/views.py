from django.shortcuts import render,redirect
from .models import Task

# Create your views here.
def index(request, config = {}):
    config['tasks'] = Task.objects.all()
    config['create_status'] = request.session.pop('create_status',None)
    config['delete_status'] = request.session.pop('delete_status',None)

    return render(request, "index.html", config)

def create(request):
    config = {}
    if request.method == "POST":
        name = request.POST['name']
        status = request.POST['status']

        duplicates_exist = Task.objects.filter(name = name).count() > 0

        if not duplicates_exist:
            task = Task(name = name, status = status)
            task.save()
            request.session['create_status'] = 'Task Successfully Added'
        else:
            request.session['create_status'] = 'Task Already Exists'
    return redirect('index')

def delete(request, task_id):
    config = {}
    if request.method == "POST":
        try:
            task = Task.objects.get(id = task_id)
            task_name = task.name
            task.delete()
            request.session['delete_status'] = f"Task {task_name} successfully deleted"
        except Task.DoesNotExist:
            request.session['delete_status'] = f"Task {task_name} failed to delete"
    return redirect('index')       


