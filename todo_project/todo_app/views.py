from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import todos
from .forms import listform

# Create your views here.
def index(request):
    if request.method=="POST":
        form=listform(request.POST or None)
        if form.is_valid:
            form.save()
            todo_list = todos.objects.all()
            return render(request, "todo_app/index.html", {'todo_list': todo_list})
    else:
        todo_list=todos.objects.all()
        return render(request,"todo_app/index.html",{'todo_list':todo_list})
def about(request):
    return render(request,"todo_app/about.html")
def create(request):
    if request.method == "POST":
        form = listform(request.POST or None)
        if form.is_valid:
            form.save()
            todo_list = todos.objects.all()
            return render(request, "todo_app/create.html", {'todo_list': todo_list})
    else:
        todo_list = todos.objects.all()
        return render(request, "todo_app/create.html", {'todo_list': todo_list})


def delete(request,todos_id):
    todo=todos.objects.get(pk=todos_id)
    todo.delete()
    return redirect("index")

def update(request,todos_id):
    if request.method=="POST":
        todo_list = todos.objects.get(pk=todos_id)
        form = listform(request.POST or None,instance=todo_list)
        if form.is_valid:
            form.save()
            return redirect("index")
    else:
        todo_item = todos.objects.get(pk=todos_id)
        return render(request, "todo_app/update.html", {'todo_item': todo_item})

def finish(request,todos_id):
    todo=todos.objects.get(pk=todos_id)
    todo.finished=False
    todo.save()
    return redirect("index")
def no_finish(request,todos_id):
    todo=todos.objects.get(pk=todos_id)
    todo.finished=True
    todo.save()
    return redirect("index")
