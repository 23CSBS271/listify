from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm, TaskForm, CategoryForm
from .models import Task, Category, ReminderLog
from .email_service import send_task_reminder_email
from django.utils import timezone

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html', {'form': form})

from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db import IntegrityError

from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import UserProfile  # import your profile model

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']  # ✅ get phone number

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username is already taken.')
            else:
                try:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    # ✅ Create or update the user's profile
                    UserProfile.objects.create(user=user, phone_number=phone_number)
                    
                    messages.success(request, "Account created successfully! Please log in.")
                    return redirect('login')
                except IntegrityError:
                    form.add_error(None, "An error occurred. Please try again.")
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})





from django.utils import timezone

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)



    # Filters
    search = request.GET.get("search", "")
    status = request.GET.get("status", "all")
    category = request.GET.get("category", "all")
    priority = request.GET.get("priority", "all")

    if search:
        tasks = tasks.filter(title__icontains=search)

    if status == "pending":
        tasks = tasks.filter(completed=False)
    elif status == "completed":
        tasks = tasks.filter(completed=True)

    if category != "all":
        if category == "none":
            tasks = tasks.filter(category__isnull=True)
        else:
            tasks = tasks.filter(category_id=category)

    if priority != "all":
        tasks = tasks.filter(priority=priority)

    # Count AFTER filtering
    stats = {
        "total": tasks.count(),
        "completed": Task.objects.filter(user=request.user, completed=True).count(),
        "pending": Task.objects.filter(user=request.user, completed=False).count(),
        "overdue": Task.objects.filter(user=request.user, completed=False, deadline__lt=timezone.now()).count()
    }

    # Pagination (optional)
    from django.core.paginator import Paginator
    paginator = Paginator(tasks, 10)
    page = request.GET.get("page")
    tasks = paginator.get_page(page)

    # Get all categories
    categories = Category.objects.filter(tasks__user=request.user).distinct()
    recent_logs = ReminderLog.objects.filter(task__user=request.user).order_by('-sent_at')[:5]


    return render(request, "dashboard.html", {
        "tasks": tasks,
        "stats": stats,
        "search": search,
        "status_filter": status,
        "category_filter": category,
        "priority_filter": priority,
        "categories": categories,
    })

# core/views.py

@login_required
def add_task(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()

        if task.reminder:
            send_task_reminder_email(
                user_email=request.user.email,
                user_name=request.user.username,
                task_title=task.title,
                task_deadline=task.deadline,
                reminder_type='deadline',
                task=task
            )

        return redirect('dashboard')

    return render(request, 'add_task.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'edit_task.html', {'form': form})

@login_required
def categories(request):
    categories = Category.objects.all()

    # Annotate user-specific task count
    for category in categories:
        category.user_task_count = category.tasks.filter(user=request.user).count()

    return render(request, 'categories.html', {
        'categories': categories
    })



@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user  # if you track owner
            category.save()
            return redirect('categories')
    else:
        form = CategoryForm()
    
    return render(request, 'add_category.html', {'form': form})

@login_required
def reminder_logs(request):
    logs = ReminderLog.objects.filter(task__user=request.user).order_by('-sent_at')
    return render(request, 'reminder_logs.html', {'logs': logs})

def logout_view(request):
    logout(request)
    return redirect('index')

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('dashboard')

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect("dashboard")
    # Optionally, if GET is used, you could show a confirmation page
    return redirect("dashboard")

from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from .forms import CategoryForm
from django.contrib.auth.decorators import login_required

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'edit_category.html', {'form': form})

from django.views.decorators.http import require_POST

@login_required
@require_POST
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('categories')

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .email_service import send_task_reminder_email

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Task, ReminderLog
from .email_service import send_task_reminder_email
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def send_test_reminder(request):
    user = request.user
    task = Task.objects.filter(user=user).first()

    if not task:
        return HttpResponse("No task available to send test reminder.")

    # Send the test email
    send_task_reminder_email(user.email, user.username, task.title, task.deadline)

    # Log it manually
    ReminderLog.objects.create(
        task=task,
        sent_at=timezone.now(),
        reminder_type='email',
        status='sent',
        message='Test reminder email sent manually.'
    )

    return redirect('reminder_logs')


# core/views.py

import calendar
from datetime import date, datetime
from collections import defaultdict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required
def calendar_view(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    cal = calendar.Calendar(firstweekday=6)  # Sunday
    month_days = list(cal.monthdatescalendar(year, month))

    tasks = Task.objects.filter(user=request.user, deadline__month=month, deadline__year=year)

    # Map tasks to dates
    task_map = defaultdict(list)
    for task in tasks:
        task.is_overdue = task.deadline < today and not task.completed
        task_map[task.deadline].append(task)

    context = {
        'month_name': calendar.month_name[month],
        'month': month,
        'year': year,
        'month_days': month_days,
        'task_map': dict(task_map),
        'today': today,
        'days_of_week': ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        'prev_month': (month - 1) or 12,
        'next_month': (month + 1) if month < 12 else 1,
        'prev_year': year - 1 if month == 1 else year,
        'next_year': year + 1 if month == 12 else year,
    }

    return render(request, 'calendar.html', context)


from django.utils import timezone
from .models import Task

def mark_overdue_tasks():
    now = timezone.now()
    Task.objects.filter(deadline__lt=now, status='pending').update(status='overdue')
