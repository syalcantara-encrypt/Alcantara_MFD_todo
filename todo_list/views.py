from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Todo
from .forms import TodoForm


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        else:

            return render(
                request,
                "login.html",
                {
                    "error": "Invalid username or password."
                }
            )

    return render(
        request,
        "login.html"
    )


def logout_view(request):

    logout(request)

    return redirect("login")


@login_required(login_url="login")
def home(request):

    todos = Todo.objects.filter(
        user=request.user
    )

    form = TodoForm()

    if request.method == "POST":

        if "add_todo" in request.POST:

            form = TodoForm(
                request.POST
            )

            if form.is_valid():

                todo = form.save(
                    commit=False
                )

                todo.user = request.user
                todo.save()

                return redirect("home")

        elif "complete_todo" in request.POST:

            todo_id = request.POST.get(
                "todo_id"
            )

            todo = get_object_or_404(
                Todo,
                id=todo_id,
                user=request.user
            )

            todo.completed = not todo.completed
            todo.save()

            return redirect("home")

        elif "delete_todo" in request.POST:

            todo_id = request.POST.get(
                "todo_id"
            )

            todo = get_object_or_404(
                Todo,
                id=todo_id,
                user=request.user
            )

            todo.delete()

            return redirect("home")

    search_query = request.GET.get(
        "search",
        ""
    )

    if search_query:

        todos = todos.filter(
            title__icontains=search_query
        )

    total_count = Todo.objects.filter(
        user=request.user
    ).count()

    completed_count = Todo.objects.filter(
        user=request.user,
        completed=True
    ).count()

    remaining_count = Todo.objects.filter(
        user=request.user,
        completed=False
    ).count()

    paginator = Paginator(
        todos,
        5
    )

    page_number = request.GET.get(
        "page"
    )

    todos = paginator.get_page(
        page_number
    )

    context = {
        "todos": todos,
        "total_count": total_count,
        "completed_count": completed_count,
        "remaining_count": remaining_count,
        "search_query": search_query,
        "form": form,
    }

    return render(
        request,
        "home.html",
        context
    )


@login_required(login_url="login")
def edit_todo(request, todo_id):

    todo = get_object_or_404(
        Todo,
        id=todo_id,
        user=request.user
    )

    form = TodoForm(
        instance=todo
    )

    if request.method == "POST":

        form = TodoForm(
            request.POST,
            instance=todo
        )

        if form.is_valid():

            form.save()

            return redirect("home")

    return render(
        request,
        "edit.html",
        {
            "todo": todo,
            "form": form
        }
    )


def about(request):

    return render(
        request,
        "about.html"
    )
