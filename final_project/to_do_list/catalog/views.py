from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import generic

from django.views.decorators.http import require_POST

from .models import TodoList, Category, Message
from django.contrib.auth.decorators import login_required


def index(request):
    todo_count = TodoList.objects.filter(user=request.user.username).count()
    categories_count = Category.objects.all().count()
    return render(
        request,
        'index.html',
        context={'todo_count': todo_count, 'categories_count': categories_count}
    )


def redirect_view(request):
    return redirect('/category')


@login_required
def todo(request):
    categories = Category.objects.all()
    user_name = request.user.username
    todos = TodoList.objects.filter(user=user_name)

    if request.method == 'POST':
        if "Add" in request.POST:
            title = request.POST['description']
            date = str(request.POST['date'])
            category = request.POST['category_select']
            content = request.POST['task_text']

            todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(name=category),
                            user=user_name)
            todo.save()
            return redirect('/catalog/todo')

        if "Delete" in request.POST:
            checkedlist = request.POST.getlist('checkedbox')

            for i in range(len(checkedlist)):
                todo = TodoList.objects.filter(id=int(checkedlist[i]))
                todo.delete()

    return render(request, "todo.html", {'todos': todos, 'categories': categories})


@login_required
def category(request):
    categories = Category.objects.all()
    if request.method == "POST":
        if "Add" in request.POST:
            name = request.POST["name"]
            category = Category(name=name)
            category.save()
            return redirect("/catalog/category")

        if "Delete" in request.POST:
            check = request.POST.getlist('check')
            for i in range(len(check)):
                сateg = Category.objects.filter(id=int(check[i]))
                сateg.delete()

    return render(request, 'category.html', {"categories": categories})


@login_required
def detail(request, todo_id):
    try:
        todo = TodoList.objects.get(id=todo_id)
    except:
        raise Http404('Task not found!')
    return render(request, 'catalog/todo_detail.html', {'todo': todo})


@login_required
@require_POST
def add_message(request, pk):
    todo = TodoList.objects.get(id=pk)
    user = request.user.username
    if request.method == 'POST':
        if "add" in request.POST:
            m1 = Message(user=user, text=request.POST['message'])
            m1.save()
            todo.message.add(m1)

            return redirect("todo-detail", todo.id)

    return render(
        request,
        'catalog/todo_detail.html',
        context={'todo': todo}
    )


class TodoDetailView(LoginRequiredMixin, generic.DetailView):
    model = TodoList
    template_name = 'catalog/todo_detail.html'

    def todo_detail_view(request, pk):
        print('IN def todo_detail_view')
        try:
            todo_id = TodoList.objects.get(id=pk)
        except TodoList.DoesNotExist:
            raise Http404("TodoList does not exist")

        return render(
            request,
            'catalog/todo_detail.html',
            context={'todo': todo_id, }
        )


class TodoListView(generic.ListView, LoginRequiredMixin):
    model = TodoList
    template_name = 'catalog/todo_list.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return TodoList.objects.all()
